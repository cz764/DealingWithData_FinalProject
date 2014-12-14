# Copyright 2013 Google Inc. All Rights Reserved.

"""Read and write properties for the CloudSDK."""

import collections
import ConfigParser
import os

from googlecloudsdk.core import config
from googlecloudsdk.core import exceptions
from googlecloudsdk.core.credentials import gce as c_gce
from googlecloudsdk.core.util import files


class Error(exceptions.Error):
  """Exceptions for the properties module."""


class PropertiesParseError(Error):
  """An exception to be raised when a properties file is invalid."""


class NoSuchPropertyError(Error):
  """An exception to be raised when the desired property does not exist."""


class MissingConfigLocationError(Error):
  """An exception to be raised when a config location does not exist."""

  def __init__(self, scope):
    super(MissingConfigLocationError, self).__init__(
        'The configuration location for [{scope}] properties does not exist.'
        .format(scope=scope.id))


class InvalidScopeValueError(Error):
  """Exception for when a string could not be parsed to a valid scope value."""

  def __init__(self, given):
    """Constructs a new exception.

    Args:
      given: str, The given string that could not be parsed.
    """
    super(InvalidScopeValueError, self).__init__(
        'Could not parse [{}] into a valid configuration scope.  '
        'Valid values are [{}]'.format(given, ', '.join(Scope.AllScopeNames())))


class InvalidValueError(Error):
  """An exception to be raised when the set value of a property is invalid."""


class RequiredPropertyError(Error):
  """Generic exception for when a required property was not set."""
  FLAG_STRING = ('It can be set on a per-command basis by re-running your '
                 'command with the [--{flag}] flag.\n\n')

  def __init__(self, prop, show_arg=False, extra_msg=None):
    section = (prop.section + '/' if prop.section != VALUES.default_section.name
               else '')
    if prop.argument and show_arg:
      flag = RequiredPropertyError.FLAG_STRING.format(
          flag=prop.argument.replace('_', '-'))
    else:
      flag = ''

    msg = ("""\
The required property [{property_name}] is not currently set.
{flag}You may set it for your current workspace by running:

  $ gcloud config set {section}{property_name} VALUE

or it can be set temporarily by the environment variable [{env_var}]"""
           .format(property_name=prop.name,
                   flag=flag,
                   section=section,
                   env_var=prop.EnvironmentName()))
    if extra_msg:
      msg += '\n\n' + extra_msg
    super(RequiredPropertyError, self).__init__(msg)
    self.property = prop


class _Sections(object):
  """Represents the available sections in the properties file.

  Attributes:
    auth: Section, The section containing auth properties for the Cloud SDK.
    default_section: Section, The main section of the properties file (core).
    core: Section, The section containing core properties for the Cloud SDK.
    component_manager: Section, The section containing properties for the
      component_manager.
  """

  def __init__(self):
    self.core = _SectionCore()
    self.component_manager = _SectionComponentManager()
    self.compute = _SectionCompute()
    self.container = _SectionContainer()
    self.auth = _SectionAuth()

    self.__sections = dict((section.name, section) for section in
                           [self.core, self.component_manager, self.compute,
                            self.container, self.auth])
    self.__args_stack = []

  @property
  def default_section(self):
    return self.core

  def __iter__(self):
    return iter(self.__sections.values())

  def GetArgsStack(self):
    return self.__args_stack

  def PushArgs(self, args):
    self.__args_stack.append(args)

  def PopArgs(self):
    self.__args_stack.pop()

  def Section(self, section):
    """Gets a section given its name.

    Args:
      section: str, The section for the desired property.

    Returns:
      Section, The section corresponding to the given name.

    Raises:
      NoSuchPropertyError: If the section is not known.
    """
    try:
      return self.__sections[section]
    except KeyError:
      raise NoSuchPropertyError('Section "{section}" does not exist.'.format(
          section=section))

  def AllSections(self):
    """Gets a list of all registered section names.

    Returns:
      [str], The section names.
    """
    return list(self.__sections.keys())

  def AllValues(self, list_unset=False, include_hidden=False):
    """Gets the entire collection of property values for all sections.

    Args:
      list_unset: bool, If True, include unset properties in the result.
      include_hidden: bool, True to include hidden properties in the result.
        If a property has a value set but is hidden, it will be included
        regardless of this setting.

    Returns:
      {str:{str:str}}, A dict of sections to dicts of properties to values.
    """
    result = {}
    for section in self:
      section_result = section.AllValues(list_unset=list_unset,
                                         include_hidden=include_hidden)
      if section_result:
        result[section.name] = section_result
    return result


class _Section(object):
  """Represents a section of the properties file that has related properties.

  Attributes:
    name: str, The name of the section.
  """

  def __init__(self, name):
    self.__name = name
    self.__properties = {}

  @property
  def name(self):
    return self.__name

  def __iter__(self):
    return iter(self.__properties.values())

  def _Add(self, name, **kwargs):
    prop = _Property(section=self.__name, name=name, **kwargs)
    self.__properties[name] = prop
    return prop

  def Property(self, property_name):
    """Gets a property from this section, given its name.

    Args:
      property_name: str, The name of the desired property.

    Returns:
      Property, The property corresponding to the given name.

    Raises:
      NoSuchPropertyError: If the property is not known for this section.
    """
    try:
      return self.__properties[property_name]
    except KeyError:
      raise NoSuchPropertyError(
          'Section "{s}" has no property "{p}".'.format(
              s=self.__name,
              p=property_name))

  def AllProperties(self, include_hidden=False):
    """Gets a list of all registered property names in this section.

    Args:
      include_hidden: bool, True to include hidden properties in the result.

    Returns:
      [str], The property names.
    """
    return [name for name, prop in self.__properties.iteritems()
            if include_hidden or not prop.is_hidden]

  def AllValues(self, list_unset=False, include_hidden=False):
    """Gets all the properties and their values for this section.

    Args:
      list_unset: bool, If True, include unset properties in the result.
      include_hidden: bool, True to include hidden properties in the result.
        If a property has a value set but is hidden, it will be included
        regardless of this setting.

    Returns:
      {str:str}, The dict of {property:value} for this section.
    """
    properties_file = _PropertiesFile.Load()
    result = {}
    for prop in self:
      if (prop.is_hidden
          and not include_hidden
          and _GetPropertyWithoutCallback(prop, properties_file) is None):
        continue
      value = _GetProperty(prop, properties_file, required=False)

      if value is None:
        if not list_unset:
          # Never include if not set and not including unset values.
          continue
        if prop.is_hidden and not include_hidden:
          # If including unset values, exclude if hidden and not including
          # hidden properties.
          continue

      # Always include if value is set (even if hidden)
      result[prop.name] = value
    return result


class _SectionCompute(_Section):
  """Contains the properties for the 'compute' section."""

  def __init__(self):
    super(_SectionCompute, self).__init__('compute')
    self.zone = self._Add('zone', argument='zone')
    self.region = self._Add('region', argument='region')


class _SectionContainer(_Section):
  """Contains the properties for the 'compute' section."""

  def __init__(self):
    super(_SectionContainer, self).__init__('container')
    self.cluster = self._Add('cluster', argument='cluster')


class _SectionCore(_Section):
  """Contains the properties for the 'core' section."""

  def __init__(self):
    super(_SectionCore, self).__init__('core')
    # pylint: disable=unnecessary-lambda, We don't want to call Metadata()
    # unless we really have to.
    self.account = self._Add(
        'account', callbacks=[lambda: c_gce.Metadata().DefaultAccount()])
    self.disable_color = self._Add('disable_color')
    self.disable_prompts = self._Add('disable_prompts', argument='quiet')
    self.disable_usage_reporting = self._Add('disable_usage_reporting')
    # pylint: disable=unnecessary-lambda, Just a value return.
    self.api_host = self._Add(
        'api_host', hidden=True,
        callbacks=[lambda: 'https://www.googleapis.com'])
    self.verbosity = self._Add('verbosity', argument='verbosity')
    self.user_output_enabled = self._Add('user_output_enabled',
                                         argument='user_output_enabled')
    # pylint: disable=unnecessary-lambda, We don't want to call Metadata()
    # unless we really have to.
    self.project = self._Add(
        'project', argument='project',
        callbacks=[lambda: c_gce.Metadata().Project()])
    self.credentialed_hosted_repo_domains = self._Add(
        'credentialed_hosted_repo_domains')


class _SectionAuth(_Section):
  """Contains the properties for the 'auth' section."""

  def __init__(self):
    super(_SectionAuth, self).__init__('auth')
    # pylint: disable=unnecessary-lambda, We don't want to call Metadata()
    # unless we really have to.
    self.auth_host = self._Add(
        'auth_host', hidden=True,
        callbacks=[lambda: 'https://accounts.google.com/o/oauth2/auth'])
    self.token_host = self._Add(
        'token_host', hidden=True,
        callbacks=[lambda: 'https://accounts.google.com/o/oauth2/token'])
    self.disable_ssl_validation = self._Add(
        'disable_ssl_validation', hidden=True)
    self.client_id = self._Add(
        'client_id', hidden=True,
        callbacks=[lambda: config.CLOUDSDK_CLIENT_ID])
    self.client_secret = self._Add(
        'client_secret', hidden=True,
        callbacks=[lambda: config.CLOUDSDK_CLIENT_NOTSOSECRET])


class _SectionComponentManager(_Section):
  """Contains the properties for the 'component_manager' section."""

  def __init__(self):
    super(_SectionComponentManager, self).__init__('component_manager')
    self.additional_repositories = self._Add('additional_repositories')
    self.disable_update_check = self._Add('disable_update_check')
    self.fixed_sdk_version = self._Add('fixed_sdk_version')
    self.snapshot_url = self._Add('snapshot_url', hidden=True)


class _Property(object):
  """An individual property that can be gotten from the properties file.

  Attributes:
    section: str, The name of the section the property appears in in the file.
    name: str, The name of the property.
    hidden: bool, True to hide this property from display.
    argument: str, The name of the command line argument that can be used to
        set this property.
    callbacks: [func], A list of functions to be called, in order, if no value
        is found elsewhere.
  """

  def __init__(self, section, name, hidden=False, argument=None,
               callbacks=None):
    self.__section = section
    self.__name = name
    self.__hidden = hidden
    self.__argument = argument
    self.__callbacks = callbacks or []

  @property
  def section(self):
    return self.__section

  @property
  def name(self):
    return self.__name

  @property
  def is_hidden(self):
    return self.__hidden

  @property
  def argument(self):
    return self.__argument

  @property
  def callbacks(self):
    return self.__callbacks

  def Get(self, required=False):
    """Gets the value for this property.

    Looks first in the environment, then in the workspace config, then in the
    global config, and finally at callbacks.

    Args:
      required: bool, True to raise an exception if the property is not set.

    Returns:
      str, The value for this property.
    """
    return _GetProperty(self, _PropertiesFile.Load(), required)

  def GetBool(self, required=False):
    """Gets the boolean value for this property.

    Looks first in the environment, then in the workspace config, then in the
    global config, and finally at callbacks.

    Args:
      required: bool, True to raise an exception if the property is not set.

    Returns:
      bool, The boolean value for this property, or None if it is not set.
    """
    return _GetBoolProperty(self, _PropertiesFile.Load(), required)

  def GetInt(self, required=False):
    """Gets the integer value for this property.

    Looks first in the environment, then in the workspace config, then in the
    global config, and finally at callbacks.

    Args:
      required: bool, True to raise an exception if the property is not set.

    Returns:
      int, The integer value for this property.
    """
    return _GetIntProperty(self, _PropertiesFile.Load(), required)

  def Set(self, value):
    """Sets the value for this property as an environment variable.

    Args:
      value: str/bool, The proposed value for this property.  If None, it is
        removed from the environment.
    """
    if value is not None:
      os.environ[self.EnvironmentName()] = str(value)
    elif self.EnvironmentName() in os.environ:
      del os.environ[self.EnvironmentName()]

  def EnvironmentName(self):
    """Get the name of the environment variable for this property.

    Returns:
      str, The name of the correct environment variable.
    """
    return 'CLOUDSDK_{section}_{name}'.format(
        section=self.__section.upper(),
        name=self.__name.upper(),
    )


VALUES = _Sections()


class Scope(object):
  """An enum class for the different types of property files that can be used.
  """
  _SCOPE_TUPLE = collections.namedtuple('_ScopeTuple',
                                        ['id', 'description', 'get_file'])
  INSTALLATION = _SCOPE_TUPLE(
      id='installation',
      description='The installation based configuration file applies to all '
      'users on the system that use this version of the Cloud SDK.  If the SDK '
      'was installed by an administrator, you will need administrator rights '
      'to make changes to this file.',
      get_file=lambda: config.Paths().installation_properties_path)
  USER = _SCOPE_TUPLE(
      id='user',
      description='The user based configuration file applies only to the '
      'current user of the system.  It will override any values from the '
      'installation configuration.',
      get_file=lambda: config.Paths().user_properties_path)
  WORKSPACE = _SCOPE_TUPLE(
      id='workspace',
      description='The workspace based configuration file is based on your '
      'current working directory.  You can set project specific configuration '
      'here that will only take effect when working within that project\'s '
      'directory.  You cannot set this value if you are not currently within a '
      'gcloud workspace.  This will override all values from any other '
      'configuration files.',
      get_file=lambda: config.Paths().workspace_properties_path)

  _ALL = [WORKSPACE, USER, INSTALLATION]
  _ALL_SCOPE_NAMES = [s.id for s in _ALL]

  @staticmethod
  def AllValues():
    """Gets all possible enum values.

    Returns:
      [Scope], All the enum values.
    """
    return list(Scope._ALL)

  @staticmethod
  def AllScopeNames():
    return list(Scope._ALL_SCOPE_NAMES)

  @staticmethod
  def FromId(scope_id):
    """Gets the enum corresponding to the given scope id.

    Args:
      scope_id: str, The scope id to parse.

    Raises:
      InvalidScopeValueError: If the given value cannot be parsed.

    Returns:
      OperatingSystemTuple, One of the OperatingSystem constants or None if the
      input is None.
    """
    if not scope_id:
      return None
    for scope in Scope._ALL:
      if scope.id == scope_id:
        return scope
    raise InvalidScopeValueError(scope_id)

  @staticmethod
  def GetHelpString():
    return '\n\n'.join(['*{0}*::: {1}'.format(s.id, s.description)
                        for s in Scope.AllValues()])


def PersistProperty(prop, value, scope=None, properties_file=None):
  """Sets the given property in the properties file.

  This function should not generally be used as part of normal program
  execution.  The property files are user editable config files that they should
  control.  This is mostly for initial setup of properties that get set during
  SDK installation.

  Args:
    prop: properties.Property, The property to set.
    value: str, The value to set for the property. If None, the property is
      removed.
    scope: Scope, The config location to set the property in.  If given, only
      this location will be udpated and it is an error if that location does
      not exist.  If not given, it will attempt to update the property in first
      the workspace config (if it exists) but then fall back to user level
      config.  It will never fall back to installation properties; you must
      use that scope explicitly to set that value.
    properties_file: str, Path to an explicit properties file to use (instead of
      one of the known locations).  It is an error to specify a scope and an
      explicit file.

  Raises:
    ValueError: If you give both a scope and a properties file.
    MissingConfigLocationError: If there is not file for the given scope.
  """
  if scope and properties_file:
    raise ValueError('You cannot provide both a scope and a specific properties'
                     ' file.')

  if not properties_file:
    if scope:
      if scope == Scope.INSTALLATION:
        config.EnsureSDKWriteAccess()
      properties_file = scope.get_file()
      if not properties_file:
        raise MissingConfigLocationError(scope)
    else:
      properties_file = Scope.WORKSPACE.get_file()
      if not properties_file:
        properties_file = Scope.USER.get_file()
        if not properties_file:
          raise MissingConfigLocationError(Scope.USER)

  parsed_config = ConfigParser.ConfigParser()
  parsed_config.read(properties_file)

  if not parsed_config.has_section(prop.section):
    if value is None:
      return
    parsed_config.add_section(prop.section)

  if value is None:
    parsed_config.remove_option(prop.section, prop.name)
  else:
    parsed_config.set(prop.section, prop.name, str(value))

  properties_dir, unused_name = os.path.split(properties_file)
  files.MakeDir(properties_dir)
  with open(properties_file, 'w') as fp:
    parsed_config.write(fp)


def _GetProperty(prop, properties_file, required):
  """Gets the given property from the properties file.

  If the property has a designated command line argument and args is provided,
  check args for the value first. If the corresponding environment variable is
  set, use that second. If still nothing, use the callbacks.

  Args:
    prop: properties.Property, The property to get.
    properties_file: _PropertiesFile, An already loaded properties files to use.
    required: bool, True to raise an exception if the property is not set.

  Raises:
    RequiredPropertyError: If the property was required but unset.

  Returns:
    str, The value of the property, or None if it is not set.
  """
  # Providing the argument overrides all.
  has_argument = False
  args_stack = VALUES.GetArgsStack()
  if prop.argument and args_stack:
    # Only check if the argument is in the first element in the stack (for the
    # purposes of error reporting.  This means the user has direct control over
    # providing this argument (as opposed to some command calling other commands
    # that the user doesn't know about.
    has_argument = args_stack[0] and hasattr(args_stack[0], prop.argument)

  value = _GetPropertyWithoutCallback(prop, properties_file)
  if value:
    return str(value)

  # Still nothing, fall back to the callbacks.
  for callback in prop.callbacks:
    value = callback()
    if value is not None:
      return str(value)

  # Not set, throw if required.
  if required:
    raise RequiredPropertyError(prop, show_arg=has_argument)

  return None


def _GetPropertyWithoutCallback(prop, properties_file):
  """Gets the given property from the properties file without using a callback.

  If the property has a designated command line argument and args is provided,
  check args for the value first. If the corresponding environment variable is
  set, use that second. If still nothing, use the callbacks.

  Args:
    prop: properties.Property, The property to get.
    properties_file: _PropertiesFile, An already loaded properties files to use.

  Returns:
    str, The value of the property, or None if it is not set.
  """
  # Providing the argument overrides all.
  args_stack = VALUES.GetArgsStack()
  if prop.argument and args_stack:
    for args in reversed(args_stack):
      if not args:
        continue
      value = getattr(args, prop.argument, None)
      if value is not None:
        return str(value)

  value = os.environ.get(prop.EnvironmentName(), None)
  if value is not None:
    return str(value)

  value = properties_file.Get(prop)
  if value is not None:
    return str(value)

  return None


def _GetBoolProperty(prop, properties_file, required):
  """Gets the given property in bool form.

  Args:
    prop: properties.Property, The property to get.
    properties_file: _PropertiesFile, An already loaded properties files to use.
    required: bool, True to raise an exception if the property is not set.

  Returns:
    bool, The value of the property, or None if it is not set.
  """
  value = _GetProperty(prop, properties_file, required)
  if value is None:
    return None
  return value.lower() in ['1', 'true', 'on', 'yes']


def _GetIntProperty(prop, properties_file, required):
  """Gets the given property in integer form.

  Args:
    prop: properties.Property, The property to get.
    properties_file: _PropertiesFile, An already loaded properties files to use.
    required: bool, True to raise an exception if the property is not set.

  Returns:
    int, The integer value of the property, or None if it is not set.
  """
  value = _GetProperty(prop, properties_file, required)
  if value is None:
    return None
  try:
    return int(value)
  except ValueError:
    raise InvalidValueError(
        'The property [{section}.{name}] must have an integer value: [{value}]'
        .format(section=prop.section, name=prop.name, value=value))


class _PropertiesFile(object):
  """Properties holder for CloudSDK CLIs."""

  @staticmethod
  def Load():
    """Loads the set of properties for the CloudSDK CLIs from files.

    This function will load the properties file, first from the installation
    config, then the global config directory CLOUDSDK_GLOBAL_CONFIG_DIR,
    and then from the workspace config directory CLOUDSDK_WORKSPACE_CONFIG_DIR.

    Returns:
      properties.Properties, The CloudSDK properties.
    """
    config_paths = config.Paths()
    paths = [config_paths.installation_properties_path,
             config_paths.user_properties_path,
             config_paths.workspace_properties_path]
    # Remove anything that was None.
    paths = [p for p in paths if p]
    return _PropertiesFile(paths)

  def __init__(self, paths):
    """Creates a new _PropertiesFile and load from the given paths.

    Args:
      paths: [str], List of files to load properties from, in order.
    """
    self._properties = {}

    for properties_path in paths:
      self.__Load(properties_path)

  def __Load(self, properties_path):
    """Loads properties from the given file.

    Overwrites anything already known.

    Args:
      properties_path: str, Path to the file containing properties info.
    """
    parsed_config = ConfigParser.ConfigParser()

    try:
      parsed_config.read(properties_path)
    except ConfigParser.ParsingError as e:
      raise PropertiesParseError(e.message)

    for section in parsed_config.sections():
      if section not in self._properties:
        self._properties[section] = {}
      self._properties[section].update(dict(parsed_config.items(section)))

  def Get(self, prop):
    """Gets the value of the given property.

    Args:
      prop: Property, The property to get.

    Returns:
      str, The value for the given section and property, or None if it is not
        set.
    """
    try:
      return self._properties[prop.section][prop.name]
    except KeyError:
      return None
