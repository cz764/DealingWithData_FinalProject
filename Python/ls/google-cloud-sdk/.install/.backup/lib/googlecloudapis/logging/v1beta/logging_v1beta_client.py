"""Generated client library for logging version v1beta."""

from googlecloudapis.apitools.base.py import base_api
from googlecloudapis.logging.v1beta import logging_v1beta_messages as messages


class LoggingV1beta(base_api.BaseApiClient):
  """Generated client library for service logging version v1beta."""

  MESSAGES_MODULE = messages

  _PACKAGE = u'logging'
  _SCOPES = [u'https://www.googleapis.com/auth/cloud-platform']
  _VERSION = u'v1beta'
  _CLIENT_ID = ''
  _CLIENT_SECRET = ''
  _USER_AGENT = ''
  _CLIENT_CLASS_NAME = u'LoggingV1beta'
  _URL_VERSION = u'v1beta'

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None):
    """Create a new logging handle."""
    url = url or u'https://www.googleapis.com/logging/v1beta/'
    super(LoggingV1beta, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers)
    self.projects_logServices_indexes = self.ProjectsLogServicesIndexesService(self)
    self.projects_logServices = self.ProjectsLogServicesService(self)
    self.projects_logs_entries = self.ProjectsLogsEntriesService(self)
    self.projects_logs_sinks = self.ProjectsLogsSinksService(self)
    self.projects_logs = self.ProjectsLogsService(self)
    self.projects = self.ProjectsService(self)

  class ProjectsLogServicesIndexesService(base_api.BaseApiService):
    """Service class for the projects_logServices_indexes resource."""

    _NAME = u'projects_logServices_indexes'

    def __init__(self, client):
      super(LoggingV1beta.ProjectsLogServicesIndexesService, self).__init__(client)
      self._method_configs = {
          'List': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'logging.projects.logServices.indexes.list',
              ordered_params=[u'service'],
              path_params=[u'service'],
              query_params=[u'depth', u'indexPrefix', u'log', u'pageSize', u'pageToken'],
              relative_path=u'{+service}/indexes',
              request_field='',
              request_type_name=u'LoggingProjectsLogServicesIndexesListRequest',
              response_type_name=u'ListLogServiceIndexesResponse',
              supports_download=False,
          ),
          }

      self._upload_configs = {
          }

    def List(self, request, global_params=None):
      """Lists log service indexes associated with a log service.

Requires https://www.googleapis.com/auth/logging.read scope.

      Args:
        request: (LoggingProjectsLogServicesIndexesListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListLogServiceIndexesResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

  class ProjectsLogServicesService(base_api.BaseApiService):
    """Service class for the projects_logServices resource."""

    _NAME = u'projects_logServices'

    def __init__(self, client):
      super(LoggingV1beta.ProjectsLogServicesService, self).__init__(client)
      self._method_configs = {
          'List': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'logging.projects.logServices.list',
              ordered_params=[u'project'],
              path_params=[u'project'],
              query_params=[u'log', u'pageSize', u'pageToken'],
              relative_path=u'{+project}/logServices',
              request_field='',
              request_type_name=u'LoggingProjectsLogServicesListRequest',
              response_type_name=u'ListLogServicesResponse',
              supports_download=False,
          ),
          }

      self._upload_configs = {
          }

    def List(self, request, global_params=None):
      """Lists log services associated with log entries ingested for a project.

Requires https://www.googleapis.com/auth/logging.read scope.

      Args:
        request: (LoggingProjectsLogServicesListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListLogServicesResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

  class ProjectsLogsEntriesService(base_api.BaseApiService):
    """Service class for the projects_logs_entries resource."""

    _NAME = u'projects_logs_entries'

    def __init__(self, client):
      super(LoggingV1beta.ProjectsLogsEntriesService, self).__init__(client)
      self._method_configs = {
          'Write': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'logging.projects.logs.entries.write',
              ordered_params=[u'log'],
              path_params=[u'log'],
              query_params=[],
              relative_path=u'{+log}/entries:write',
              request_field=u'writeLogEntriesRequest',
              request_type_name=u'LoggingProjectsLogsEntriesWriteRequest',
              response_type_name=u'LoggingProjectsLogsEntriesWriteResponse',
              supports_download=False,
          ),
          }

      self._upload_configs = {
          }

    def Write(self, request, global_params=None):
      """Creates several log entries in a log.

Requires https://www.googleapis.com/auth/logging.write scope.

      Args:
        request: (LoggingProjectsLogsEntriesWriteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (LoggingProjectsLogsEntriesWriteResponse) The response message.
      """
      config = self.GetMethodConfig('Write')
      return self._RunMethod(
          config, request, global_params=global_params)

  class ProjectsLogsSinksService(base_api.BaseApiService):
    """Service class for the projects_logs_sinks resource."""

    _NAME = u'projects_logs_sinks'

    def __init__(self, client):
      super(LoggingV1beta.ProjectsLogsSinksService, self).__init__(client)
      self._method_configs = {
          'Delete': base_api.ApiMethodInfo(
              http_method=u'DELETE',
              method_id=u'logging.projects.logs.sinks.delete',
              ordered_params=[u'sink'],
              path_params=[u'sink'],
              query_params=[],
              relative_path=u'{+sink}',
              request_field='',
              request_type_name=u'LoggingProjectsLogsSinksDeleteRequest',
              response_type_name=u'LoggingProjectsLogsSinksDeleteResponse',
              supports_download=False,
          ),
          'Get': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'logging.projects.logs.sinks.get',
              ordered_params=[u'sink'],
              path_params=[u'sink'],
              query_params=[],
              relative_path=u'{+sink}',
              request_field='',
              request_type_name=u'LoggingProjectsLogsSinksGetRequest',
              response_type_name=u'LogSink',
              supports_download=False,
          ),
          'List': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'logging.projects.logs.sinks.list',
              ordered_params=[u'log'],
              path_params=[u'log'],
              query_params=[],
              relative_path=u'{+log}/sinks',
              request_field='',
              request_type_name=u'LoggingProjectsLogsSinksListRequest',
              response_type_name=u'ListLogSinksResponse',
              supports_download=False,
          ),
          'Patch': base_api.ApiMethodInfo(
              http_method=u'PATCH',
              method_id=u'logging.projects.logs.sinks.patch',
              ordered_params=[u'sink'],
              path_params=[u'sink'],
              query_params=[],
              relative_path=u'{+sink}',
              request_field=u'logSink',
              request_type_name=u'LoggingProjectsLogsSinksPatchRequest',
              response_type_name=u'LogSink',
              supports_download=False,
          ),
          'Update': base_api.ApiMethodInfo(
              http_method=u'PUT',
              method_id=u'logging.projects.logs.sinks.update',
              ordered_params=[u'sink'],
              path_params=[u'sink'],
              query_params=[],
              relative_path=u'{+sink}',
              request_field=u'logSink',
              request_type_name=u'LoggingProjectsLogsSinksUpdateRequest',
              response_type_name=u'LogSink',
              supports_download=False,
          ),
          }

      self._upload_configs = {
          }

    def Delete(self, request, global_params=None):
      """Deletes the specified log sink. Requires https://www.googleapis.com/auth/logging.admin scope.

      Args:
        request: (LoggingProjectsLogsSinksDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (LoggingProjectsLogsSinksDeleteResponse) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Get(self, request, global_params=None):
      """Get the specified log sink resource. Requires https://www.googleapis.com/auth/logging.read scope.

      Args:
        request: (LoggingProjectsLogsSinksGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (LogSink) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    def List(self, request, global_params=None):
      """List log sinks associated with the specified log. Requires https://www.googleapis.com/auth/logging.read scope.

      Args:
        request: (LoggingProjectsLogsSinksListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListLogSinksResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Patch(self, request, global_params=None):
      """Create or update the specified log sink resource. Requires https://www.googleapis.com/auth/logging.admin scope. This method supports patch semantics.

      Args:
        request: (LoggingProjectsLogsSinksPatchRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (LogSink) The response message.
      """
      config = self.GetMethodConfig('Patch')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Update(self, request, global_params=None):
      """Create or update the specified log sink resource. Requires https://www.googleapis.com/auth/logging.admin scope.

      Args:
        request: (LoggingProjectsLogsSinksUpdateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (LogSink) The response message.
      """
      config = self.GetMethodConfig('Update')
      return self._RunMethod(
          config, request, global_params=global_params)

  class ProjectsLogsService(base_api.BaseApiService):
    """Service class for the projects_logs resource."""

    _NAME = u'projects_logs'

    def __init__(self, client):
      super(LoggingV1beta.ProjectsLogsService, self).__init__(client)
      self._method_configs = {
          'List': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'logging.projects.logs.list',
              ordered_params=[u'project'],
              path_params=[u'project'],
              query_params=[u'pageSize', u'pageToken', u'serviceIndexPrefix', u'serviceName'],
              relative_path=u'{+project}/logs',
              request_field='',
              request_type_name=u'LoggingProjectsLogsListRequest',
              response_type_name=u'ListLogsResponse',
              supports_download=False,
          ),
          }

      self._upload_configs = {
          }

    def List(self, request, global_params=None):
      """Lists log resources belonging to the specified project.

Requires https://www.googleapis.com/auth/logging.read scope.

      Args:
        request: (LoggingProjectsLogsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListLogsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = u'projects'

    def __init__(self, client):
      super(LoggingV1beta.ProjectsService, self).__init__(client)
      self._method_configs = {
          }

      self._upload_configs = {
          }
