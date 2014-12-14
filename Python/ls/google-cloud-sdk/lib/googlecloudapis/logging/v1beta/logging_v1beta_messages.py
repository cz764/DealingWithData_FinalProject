"""Generated message classes for logging version v1beta.

Read and write access to logged events.
"""

from protorpc import messages


package = 'logging'


class Any(messages.Message):
  """Any contains an arbitrary serialized message along with a URL that
  describes the type of the serialized message.

  Fields:
    typeUrl: A URL that resolves to a google.protobuf.Type value.
    value: Serialized data of the specified type.  Note: the field is optional
      since if we are converting between formats and the type could not be
      resolved, we store the original data pre-conversion in other fields
      (TBD).
  """

  typeUrl = messages.StringField(1)
  value = messages.BytesField(2)


class ListLogServiceIndexesResponse(messages.Message):
  """Result returned from ListLogServiceIndexesRequest.

  Fields:
    nextPageToken: A token to retrieve more log service indexes. If
      next_page_token is not empty, addition results may be retrieved by
      calling ListLogServiceIndexes again with page_token set to this value.
    serviceIndexPrefixes: A list of log service index prefixes.
  """

  nextPageToken = messages.StringField(1)
  serviceIndexPrefixes = messages.StringField(2, repeated=True)


class ListLogServicesResponse(messages.Message):
  """Result returned from ListLogServicesRequest.

  Fields:
    logServices: A list of log services.
    nextPageToken: A token to retrieve more ServiceIndex objects. If
      next_page_token is not empty, addition results may be retrieved by
      calling ListLogServices again with page_token set to this value.
  """

  logServices = messages.MessageField('LogService', 1, repeated=True)
  nextPageToken = messages.StringField(2)


class ListLogSinksResponse(messages.Message):
  """Result returned from ListLogSinks.

  Fields:
    sinks: These may be partial sinks where only name is populated.
  """

  sinks = messages.MessageField('LogSink', 1, repeated=True)


class ListLogsResponse(messages.Message):
  """Result returned from ListLogs.

  Fields:
    logs: A list of log resources.
    nextPageToken: Pagination: If there are more results, retrieve them by
      invoking ListLogs again with the same arguments and this
      next_page_token.
  """

  logs = messages.MessageField('Log', 1, repeated=True)
  nextPageToken = messages.StringField(2)


class Log(messages.Message):
  """A log object.

  Fields:
    displayName: Name to be used when displaying the log to the user (e.g., in
      a UI)
    name: REQUIRED: log name
    payloadType: Type URL describing the expected payload type for the log.
  """

  displayName = messages.StringField(1)
  name = messages.StringField(2)
  payloadType = messages.StringField(3)


class LogEntry(messages.Message):
  """An individual entry in a log.

  Fields:
    insertId: Unique ID used to deduplicate log entries. If provided, the
      logging service will attempt to reject multiple log entries on the same
      log with the same insert_id that are sent within the previous N minutes.
      Deduplication may occur asynchronously, so the client may not receive an
      error if the entry is recognized as a duplicate.
    log: The log resource that this entry belongs to. This is ignored by
      WriteLogEntries (the log name is instead specified in the URL).
    metadata: Metadata for the log entry.
    protoPayload: Contains a structured (protocol buffer) log entry. If the
      data type in proto_payload is known by the logging system, JSON clients
      will receive it in JSON; otherwise, the client will receive it as a
      serialized proto and must decode it. See google.protobuf.Any for more
      details.
    textPayload: Contains a text representation of the log entry.
  """

  insertId = messages.StringField(1)
  log = messages.StringField(2)
  metadata = messages.MessageField('LogEntryMetadata', 3)
  protoPayload = messages.MessageField('Any', 4)
  textPayload = messages.StringField(5)


class LogEntryMetadata(messages.Message):
  """Additional data that is associated with a log entry.

  Enums:
    SeverityValueValuesEnum: The severity of the log entry.

  Fields:
    labels: Callers are expected to populate one of the following sets of
      labels describing the source of the log entry.  App Engine: service:
      "appengine.googleapis.com" labels: appengine.googleapis.com/module_id
      appengine.googleapis.com/version_id and one of:
      appengine.googleapis.com/replica_index appengine.googleapis.com/clone_id
      or the Compute Engine labels (resource_type/resource_id) below  Compute
      Engine: service: "compute.googleapis.com" labels:
      compute.googleapis.com/resource_type = "instance"
      compute.googleapis.com/resource_id
    projectId: If the log entry is from a Google Cloud Platform source, this
      must be the project ID of the service that generated the entry.
      Otherwise, the caller may populate this with whatever project name or ID
      is meaningful, or leave it unset.
    projectNumber: This field is populated by the API at ingestion time
    region: If the log entry is from a Google Cloud Platform source, this must
      be the region of the source (e.g., us-central1) if it has one, or unset
      if "region" isn't meaningful for the service.  For non-Google Cloud
      Platform sources, the caller may populate this with whatever location
      name is meaningful, or leave it unset.
    serviceName: If the log entry is from a Google Cloud Platform source, this
      must be the official API name of the service (e.g.,
      compute.googleapis.com). Otherwise, the caller may populate this with
      whatever service name is meaningful, or leave it unset.
    severity: The severity of the log entry.
    timeNanos: REQUIRED: The time the event described by the log entry
      occurred, in nanoseconds since the Unix epoch.
    timestamp: REQUIRED: The time the event described by the log entry
      occurred.
    userId: If the log entry applies to an action taken by an authenticated
      user, this field must contain the user identifier (a fully qualified
      email address) of the user that requested or performed the action. May
      be empty if the event described by the log entry doesn't have an
      associated user.
    zone: If the log entry is from a Google Cloud Platform source, this must
      be the zone of the source (e.g., us-central1-a) if it has one, or unset
      if "zone" isn't meaningful for the service.  For non-Google Cloud
      Platform sources, the caller may populate this with whatever location
      name is meaningful, or leave it unset.
  """

  class SeverityValueValuesEnum(messages.Enum):
    """The severity of the log entry.

    Values:
      alert: <no description>
      critical: <no description>
      debug: <no description>
      default: <no description>
      emergency: <no description>
      error: <no description>
      info: <no description>
      notice: <no description>
      warning: <no description>
    """
    alert = 0
    critical = 1
    debug = 2
    default = 3
    emergency = 4
    error = 5
    info = 6
    notice = 7
    warning = 8

  labels = messages.MessageField('LogEntryMetadataLabelsEntry', 1, repeated=True)
  projectId = messages.StringField(2)
  projectNumber = messages.IntegerField(3)
  region = messages.StringField(4)
  serviceName = messages.StringField(5)
  severity = messages.EnumField('SeverityValueValuesEnum', 6)
  timeNanos = messages.IntegerField(7)
  timestamp = messages.MessageField('Timestamp', 8)
  userId = messages.StringField(9)
  zone = messages.StringField(10)


class LogEntryMetadataLabelsEntry(messages.Message):
  """A LogEntryMetadataLabelsEntry object.

  Fields:
    key: A string attribute.
    value: A string attribute.
  """

  key = messages.StringField(1)
  value = messages.StringField(2)


class LogError(messages.Message):
  """An object that describes a problem in a sink or the sink's configuration.

  Fields:
    resource: The resource associated with the error. It may be different from
      the sink destination. E.g. the sink may point to a BigQuery dataset, but
      the error may refer to a table resource inside the dataset.
    status: The description of the last error observed.
    timeNanos: The last time the error was observed, in nanoseconds since the
      Unix epoch.
  """

  resource = messages.StringField(1)
  status = messages.MessageField('Status', 2)
  timeNanos = messages.IntegerField(3)


class LogService(messages.Message):
  """A log service object.

  Fields:
    indexKeys: Label keys used when labeling log entries for this service. The
      order of the keys is significant, with higher priority keys coming
      earlier in the list.
    name: The service's name.
  """

  indexKeys = messages.StringField(1, repeated=True)
  name = messages.StringField(2)


class LogSink(messages.Message):
  """An object that describes where a log may be written.

  Fields:
    destination: The resource to send log entries to. The supported sink
      resource types are:  Google Cloud Storage:
      storage.googleapis.com/{bucket} bucket.storage.googleapis.com/ Google
      BigQuery:
      bigquery.googleapis.com/projects/{projectId}/datasets/{datasetId}
      Currently the logging service supports at most one sink of each type per
      log resource.
    errors: All active errors found for this sink. [output only]
    name: The name of this sink. This is a client-assigned identifier for the
      resource.
  """

  destination = messages.StringField(1)
  errors = messages.MessageField('LogError', 2, repeated=True)
  name = messages.StringField(3)


class LoggingProjectsLogServicesIndexesListRequest(messages.Message):
  """A LoggingProjectsLogServicesIndexesListRequest object.

  Fields:
    depth: A limit to the number of levels of the index hierarchy that will be
      expanded. If the depth is 0, it will default to the level specified by
      the prefix field (the number of slash separators). The default empty
      prefix implies a depth of 1. It is an error for depth to be any non-zero
      value less than the number of components in index_prefix.
    indexPrefix: A prefix of the log service indexes to be returned. The
      prefix is a slash separated list of the label values in order
      corresponding to the [LogService
      index_keys][google.logging.v1.LogService.index_keys]. For example use
      "/myModule/" to retrieve App Engine versions associated with myModule.
      The trailing slash terminates the value, while "/myModule" would allow
      retrieval of App Engine modules with names beginning with myModule. An
      prefix component matches all log service indexes. A non-empty prefix
      must begin with "/".
    log: A log resource like /projects/project_id/logs/log_name identifying
      the log for which to list services indexes.
    pageSize: The maximum number of log service index resources to return.
    pageToken: An optional next_page_token from a previous
      ListLogServicesIndexesResult. Other fields are ignored when the
      page_token is not empty.
    service: A log service resource whose service indexes to return (e.g.
      /projects/myProj/logServices/appengine.googleapis.com).
  """

  depth = messages.IntegerField(1, variant=messages.Variant.INT32)
  indexPrefix = messages.StringField(2)
  log = messages.StringField(3)
  pageSize = messages.IntegerField(4, variant=messages.Variant.INT32)
  pageToken = messages.StringField(5)
  service = messages.StringField(6, required=True)


class LoggingProjectsLogServicesListRequest(messages.Message):
  """A LoggingProjectsLogServicesListRequest object.

  Fields:
    log: A log resource like /projects/project_id/logs/log_name identifying
      the log for which to list services. When empty, all services will be
      listed.
    pageSize: The maximum number of LogService objects to return.
    pageToken: An optional next_page_token from a previous
      ListLogServicesResult. Other fields are ignored when the page_token is
      not empty.
    project: The project resource for which to list the services.
  """

  log = messages.StringField(1)
  pageSize = messages.IntegerField(2, variant=messages.Variant.INT32)
  pageToken = messages.StringField(3)
  project = messages.StringField(4, required=True)


class LoggingProjectsLogsEntriesWriteRequest(messages.Message):
  """A LoggingProjectsLogsEntriesWriteRequest object.

  Fields:
    log: The log resource into which to insert the log entries.
    writeLogEntriesRequest: A WriteLogEntriesRequest resource to be passed as
      the request body.
  """

  log = messages.StringField(1, required=True)
  writeLogEntriesRequest = messages.MessageField('WriteLogEntriesRequest', 2)


class LoggingProjectsLogsEntriesWriteResponse(messages.Message):
  """An empty LoggingProjectsLogsEntriesWrite response."""


class LoggingProjectsLogsListRequest(messages.Message):
  """A LoggingProjectsLogsListRequest object.

  Fields:
    pageSize: Pagination: maximum number of results to return per page
    pageToken: Pagination: a next_page_token previously returned from ListLogs
    project: The project ID for which to list the log resources.
    serviceIndexPrefix: A log service index prefix for which to list logs.
      Only logs containing entries whose metadata included these label values
      (associated with index keys) will be returned. The prefix is a slash
      separated list of values, and need not specify all index labels. An
      empty index (the default) matches all log service indexes. It is an
      error to provide a non-empty service_index_prefix with an empty
      service_name.
    serviceName: A service name for which to list logs. Only logs containing
      entries whose metadata included this service name will be returned. If
      empty, logs associated with all services are returned.
  """

  pageSize = messages.IntegerField(1, variant=messages.Variant.INT32)
  pageToken = messages.StringField(2)
  project = messages.StringField(3, required=True)
  serviceIndexPrefix = messages.StringField(4)
  serviceName = messages.StringField(5)


class LoggingProjectsLogsSinksDeleteRequest(messages.Message):
  """A LoggingProjectsLogsSinksDeleteRequest object.

  Fields:
    sink: The sink to delete.
  """

  sink = messages.StringField(1, required=True)


class LoggingProjectsLogsSinksDeleteResponse(messages.Message):
  """An empty LoggingProjectsLogsSinksDelete response."""


class LoggingProjectsLogsSinksGetRequest(messages.Message):
  """A LoggingProjectsLogsSinksGetRequest object.

  Fields:
    sink: The sink to return.
  """

  sink = messages.StringField(1, required=True)


class LoggingProjectsLogsSinksListRequest(messages.Message):
  """A LoggingProjectsLogsSinksListRequest object.

  Fields:
    log: The log for which to list sinks.
  """

  log = messages.StringField(1, required=True)


class LoggingProjectsLogsSinksPatchRequest(messages.Message):
  """A LoggingProjectsLogsSinksPatchRequest object.

  Fields:
    logSink: A LogSink resource to be passed as the request body.
    sink: The sink to update.
  """

  logSink = messages.MessageField('LogSink', 1)
  sink = messages.StringField(2, required=True)


class LoggingProjectsLogsSinksUpdateRequest(messages.Message):
  """A LoggingProjectsLogsSinksUpdateRequest object.

  Fields:
    logSink: A LogSink resource to be passed as the request body.
    sink: The sink to update.
  """

  logSink = messages.MessageField('LogSink', 1)
  sink = messages.StringField(2, required=True)


class StandardQueryParameters(messages.Message):
  """Query parameters accepted by all methods.

  Enums:
    AltValueValuesEnum: Data format for the response.

  Fields:
    alt: Data format for the response.
    fields: Selector specifying which fields to include in a partial response.
    key: API key. Your API key identifies your project and provides you with
      API access, quota, and reports. Required unless you provide an OAuth 2.0
      token.
    oauth_token: OAuth 2.0 token for the current user.
    prettyPrint: Returns response with indentations and line breaks.
    quotaUser: Available to use for quota purposes for server-side
      applications. Can be any arbitrary string assigned to a user, but should
      not exceed 40 characters. Overrides userIp if both are provided.
    trace: A tracing token of the form "token:<tokenid>" or "email:<ldap>" to
      include in api requests.
    userIp: IP address of the site where the request originates. Use this if
      you want to enforce per-user limits.
  """

  class AltValueValuesEnum(messages.Enum):
    """Data format for the response.

    Values:
      json: Responses with Content-Type of application/json
    """
    json = 0

  alt = messages.EnumField('AltValueValuesEnum', 1, default=u'json')
  fields = messages.StringField(2)
  key = messages.StringField(3)
  oauth_token = messages.StringField(4)
  prettyPrint = messages.BooleanField(5, default=True)
  quotaUser = messages.StringField(6)
  trace = messages.StringField(7)
  userIp = messages.StringField(8)


class Status(messages.Message):
  """Represents RPC error status for One Platform APIs.

  Fields:
    code: The status code, which should be an enum value of
      [google.rpc.Code][].
    details: A list of messages that carry the error details. There will be a
      common set of message types for APIs to use.
    message: A developer-facing error message, which should be in English. The
      user- facing error message should be localized and stored in the
      [google.rpc.Status.details][] field.
  """

  code = messages.IntegerField(1, variant=messages.Variant.INT32)
  details = messages.MessageField('Any', 2, repeated=True)
  message = messages.StringField(3)


class Timestamp(messages.Message):
  """A Timestamp represents a point in time independent of any time zone or
  calendar, represented as seconds and fractions of seconds at nanosecond
  resolution in UTC Epoch time. It is encoded using the Proleptic Gregorian
  Calendar which extends the Gregorian calendar backwards to year one. It is
  encoded assuming all minutes are 60 seconds long, i.e. leap seconds are
  "smeared" so that no leap second table is needed for interpretation. Range
  is from 0001-01-01T00:00:00Z to 9999-12-31T23:59:59.999999999Z.  Example 1:
  compute Timestamp from POSIX `time()`.  Timestamp timestamp;
  timestamp.set_seconds(time(NULL)); timestamp.set_nanos(0);  Example 2:
  compute Timestamp from POSIX `gettimeofday()`.  struct timeval tv;
  gettimeofday(&tv, NULL);  Timestamp timestamp;
  timestamp.set_seconds(tv.tv_sec); timestamp.set_nanos(tv.tv_usec * 1000);
  Example 3: compute Timestamp from Win32 `GetSystemTimeAsFileTime()`.
  FILETIME ft; GetSystemTimeAsFileTime(&ft); UINT64 ticks =
  (((UINT64)ft.dwHighDateTime) << 32) | ft.dwLowDateTime;  // A Windows tick
  is 100 nanoseconds. Windows epoch 1601-01-01T00:00:00Z // is 11644473600
  seconds before Unix epoch 1970-01-01T00:00:00Z. Timestamp timestamp;
  timestamp.set_seconds((INT64) ((ticks / 10000000) - 11644473600LL));
  timestamp.set_nanos((INT32) ((ticks % 10000000) * 100));  Example 4: compute
  Timestamp from Java `System.currentTimeMillis()`.  long millis =
  System.currentTimeMillis();  Timestamp timestamp =
  Timestamp.newBuilder().setSeconds(millis / 1000) .setNanos((int) ((millis %
  1000) * 1000000)).build();  Example 5: compute Timestamp from Python
  `datetime.datetime`.  now = datetime.datetime.utcnow() seconds =
  int(time.mktime(now.timetuple())) nanos = now.microsecond * 1000 timestamp =
  Timestamp(seconds=seconds, nanos=nanos)

  Fields:
    nanos: Positive fractions of a second at nanosecond resolution. Negative
      second values with fractions may still have positive nanos values that
      count forward in time. Must be from 0 to 999,999,999 inclusive.
    seconds: Positive or negative seconds of UTC time since Unix epoch
      1970-01-01T00:00:00Z. Must be from from 0001-01-01T00:00:00Z to
      9999-12-31T23:59:59Z inclusive.
  """

  nanos = messages.IntegerField(1, variant=messages.Variant.INT32)
  seconds = messages.IntegerField(2)


class WriteLogEntriesRequest(messages.Message):
  """The parameters to WriteLogEntries.

  Fields:
    commonLabels: Labels that apply to all entries in this request. If a
      conflicting label key is present in the per-entry LogEntryMetadata.label
      list, it overrides the value specified here.  See the documentation for
      LogEntryMetadata.labels for additional notes.
    entries: Log entries to insert.
  """

  commonLabels = messages.MessageField('WriteLogEntriesRequestCommonLabelsEntry', 1, repeated=True)
  entries = messages.MessageField('LogEntry', 2, repeated=True)


class WriteLogEntriesRequestCommonLabelsEntry(messages.Message):
  """A WriteLogEntriesRequestCommonLabelsEntry object.

  Fields:
    key: A string attribute.
    value: A string attribute.
  """

  key = messages.StringField(1)
  value = messages.StringField(2)


