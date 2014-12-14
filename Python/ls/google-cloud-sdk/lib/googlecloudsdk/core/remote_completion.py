# Copyright 2014 Google Inc. All Rights Reserved.
"""Remote resource completion and caching."""
import logging
import os
import time

from googlecloudsdk.core import config
from googlecloudsdk.core import properties


class RemoteCompletion(object):
  """Class to cache the names of remote resources."""

  CACHE_HITS = 0
  CACHE_TRIES = 0
  _TIMEOUTS = {  # Timeouts for resources in seconds
      'instances': 600,
      'region': 3600*10,
      'zone': 3600*10
  }
  _ITEM_NAME_FUN = {
      'compute': lambda item: item['name'],
      'sql': lambda item: item.instance
  }

  def __init__(self):
    """Set the cache directory."""
    self.project = properties.VALUES.core.project.Get(required=True)
    self.cache_dir = config.Paths().completion_cache_dir

  def CachePath(self, resource, zoneregion):
    """Creates a pathname for the resource.

    Args:
      resource: The resource as subcommand.resource.
      zoneregion: The zone or region name.

    Returns:
      Returns a pathname for the resource.
    """
    path = os.path.join(self.cache_dir, resource, self.project)
    if zoneregion:
      path = os.path.join(path, zoneregion)
    return path

  def GetFromCache(self, resource, zoneregion=None):
    """Return a list of names for the resource and zoneregion.

    Args:
      resource: The resource as subcommand.resource.
      zoneregion: The zone or region name or None.

    Returns:
      Returns a list of names if in the cache.
    """
    options = []
    RemoteCompletion.CACHE_TRIES += 1
    if not zoneregion:
      zoneregion = '_ALL_ZONES'
    fpath = self.CachePath(resource, zoneregion)
    try:
      if os.path.getmtime(fpath) > time.time():
        with open(fpath, 'r') as f:
          line = f.read().rstrip('\n')
        options = line.split(' ')
        RemoteCompletion.CACHE_HITS += 1
        return options
    except Exception:  # pylint:disable=broad-except
      return None
    return None

  def StoreInCache(self, resource, options, zoneregion):
    """Return the list of names for the resource and zoneregion.

    Args:
      resource: The resource as subcommand.resource.
      options: A list of possible completions.
      zoneregion: The zone or region name, or None if no zone or region.

    Returns:
      None
    """
    path = self.CachePath(resource, zoneregion)
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
      os.makedirs(dirname)
    if options:
      with open(path, 'w') as f:
        f.write(' '.join(options) + '\n')
    now = time.time()
    if options is None:
      timeout = 0
    else:
      timeout = RemoteCompletion._TIMEOUTS.get(resource, 300)
    os.utime(path, (now, now+timeout))

  @staticmethod
  def GetCompleterForResource(resource, cli):
    """Returns a completer function for the give resource.

    Args:
      resource: The resource as subcommand.resource.
      cli: The calliope instance.

    Returns:
      A completer function for the specified resource.
    """

    def RemoteCompleter(parsed_args, **unused_kwargs):
      """Run list command on  resource to generates completion options."""
      options = []
      try:
        command = resource.split('.') + ['list']
        zoneregion = None
        if command[0] == 'compute':
          zoneregion = '_ALL_ZONES'
        if hasattr(parsed_args, 'zone') and parsed_args.zone:
          zoneregion = parsed_args.zone
          command.append('--zone')
          command.append(zoneregion)
        if hasattr(parsed_args, 'region') and parsed_args.region:
          zoneregion = parsed_args.region
          command.append('--region')
          command.append(zoneregion)
        ccache = RemoteCompletion()
        options = ccache.GetFromCache(resource, zoneregion)
        if options is None:
          properties.VALUES.core.user_output_enabled.Set(False)
          items = list(cli().Execute(command, call_arg_complete=False))
          fun = RemoteCompletion._ITEM_NAME_FUN[command[0]]
          options = [fun(item) for item in items]
          ccache.StoreInCache(resource, options, zoneregion)
      except Exception:  # pylint:disable=broad-except
        logging.error(resource + 'completion command failed', exc_info=True)
        return None
      return options
    return RemoteCompleter

