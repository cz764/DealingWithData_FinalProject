# Copyright 2014 Google Inc. All Rights Reserved.

"""Helper methods for importing record-sets."""

from dns import rdatatype
from dns import zone

import yaml

from googlecloudsdk.apis.dns.v1beta1 import dns_v1beta1_messages as messages
from googlecloudsdk.calliope import exceptions


# pylint:disable=unused-argument, Origin is required just to have a
# uniform signature for all translations.
def _AddressTranslation(rdata, unused_origin):
  """Returns the address of the given rdata.

  Args:
    rdata: Rdata, The data to be translated.
    unused_origin: Name, The origin domain name.

  Returns:
    str, The address of the given rdata.
  """
  return rdata.address


def _MXTranslation(rdata, origin):
  """Returns the translation of the given MX rdata.

  Args:
    rdata: Rdata, The data to be translated.
    origin: Name, The origin domain name.

  Returns:
    str, The translation of the given MX rdata which includes the preference and
    qualified exchange name.
  """
  return '{0} {1}'.format(rdata.preference, rdata.exchange.derelativize(origin))


def _SOATranslation(rdata, origin):
  """Returns the translation of the given SOA rdata.

  Args:
    rdata: Rdata, The data to be translated.
    origin: Name, The origin domain name.

  Returns:
    str, The translation of the given SOA rdata which includes all the required
    SOA fields. Note that the master NS name is left in a substitutable form
    because it is always provided by Cloud DNS.
  """
  return ' '.join(
      [str(x) for x in [
          '{0}',
          rdata.rname.derelativize(origin),
          rdata.serial,
          rdata.refresh,
          rdata.retry,
          rdata.expire,
          rdata.minimum]])


def _SRVTranslation(rdata, origin):
  """Returns the translation of the given SRV rdata.

  Args:
    rdata: Rdata, The data to be translated.
    origin: Name, The origin domain name.

  Returns:
    str, The translation of the given SRV rdata which includes all the required
    SRV fields. Note that the translated target name is always qualified.
  """
  return ' '.join(
      [str(x) for x in [
          rdata.priority,
          rdata.weight,
          rdata.port,
          rdata.target.derelativize(origin)]])


def _TargetTranslation(rdata, origin):
  """Returns the qualified target of the given rdata.

  Args:
    rdata: Rdata, The data to be translated.
    origin: Name, The origin domain name.

  Returns:
    str, The qualified target of the given rdata.
  """
  return rdata.target.derelativize(origin).to_text()


def _EscapedText(text):
  """Returns the given text within quotes.

  Args:
    text: str, The text to be escaped.

  Returns:
    str, The given text within quotes.
  """
  if text.startswith('"') and text.endswith('"'):
    # Nothing to do if already escaped.
    return text
  else:
    return '\"{0}\"'.format(text)


def _EscapedTextTranslation(rdata, unused_origin):
  """Returns the escaped translation of the given text rdata.

  Args:
    rdata: Rdata, The data to be translated.
    unused_origin: Name, The origin domain name.

  Returns:
    str, The translation of the given text rdata, which is the concatenation of
    all its strings. The result is escaped with quotes. For further details,
    please refer to the TXT section at:
    https://cloud.google.com/dns/what-is-cloud-dns#supported_record_types.
  """
  return ' '.join([_EscapedText(string) for string in rdata.strings])


# Map of functions for translating rdata for various record types from zone
# format to Cloud DNS format.
_RDATA_TRANSLATIONS = {
    rdatatype.A: _AddressTranslation,
    rdatatype.AAAA: _AddressTranslation,
    rdatatype.CNAME: _TargetTranslation,
    rdatatype.MX: _MXTranslation,
    rdatatype.PTR: _TargetTranslation,
    rdatatype.SOA: _SOATranslation,
    rdatatype.SPF: _EscapedTextTranslation,
    rdatatype.SRV: _SRVTranslation,
    rdatatype.TXT: _EscapedTextTranslation,
}


def _RecordSetFromZoneRecord(name, rdset, origin):
  """Returns the Cloud DNS ResourceRecordSet for the given zone file record.

  Args:
    name: Name, Domain name of the zone record.
    rdset: Rdataset, The zone record object.
    origin: Name, The origin domain of the zone file.

  Returns:
    The ResourceRecordSet equivalent for the given zone record, or None for
    unsupported record types.
  """
  if rdset.rdtype not in _RDATA_TRANSLATIONS:
    return None

  record_set = messages.ResourceRecordSet()
  # Need to assign kind to default value for useful equals comparisons.
  record_set.kind = record_set.kind
  record_set.name = name.derelativize(origin).to_text()
  record_set.ttl = rdset.ttl
  record_set.type = rdatatype.to_text(rdset.rdtype)
  rdatas = []
  for rdata in rdset:
    rdatas.append(_RDATA_TRANSLATIONS[rdset.rdtype](rdata, origin))
  record_set.rrdatas = rdatas
  return record_set


def RecordSetsFromZoneFile(zone_file, domain):
  """Returns record-sets for the given domain imported from the given zone file.

  Args:
    zone_file: file, The zone file with records for the given domain.
    domain: str, The domain for which record-sets should be obtained.

  Returns:
    A (name, type) keyed dict of ResourceRecordSets that were obtained from the
    zone file. Note that only A, AAAA, CNAME, MX, PTR, SOA, SPF, SRV, and TXT
    record-sets are retrieved. Other record-set types are not supported by Cloud
    DNS. Also, the master NS field for SOA records is discarded since that is
    provided by Cloud DNS.
  """
  zone_contents = zone.from_file(zone_file, domain, check_origin=False)
  record_sets = {}
  for name, rdset in zone_contents.iterate_rdatasets():
    record_set = _RecordSetFromZoneRecord(name, rdset, zone_contents.origin)
    if record_set:
      record_sets[(record_set.name, record_set.type)] = record_set
  return record_sets


def RecordSetsFromYamlFile(yaml_file):
  """Returns record-sets read from the given yaml file.

  Args:
    yaml_file: file, A yaml file with records.

  Returns:
    A (name, type) keyed dict of ResourceRecordSets that were obtained from the
    yaml file. Note that only A, AAAA, CNAME, MX, PTR, SOA, SPF, SRV, and TXT
    record-sets are retrieved. Other record-set types are not supported by Cloud
    DNS. Also, the master NS field for SOA records is discarded since that is
    provided by Cloud DNS.
  """
  record_sets = {}

  yaml_record_sets = yaml.safe_load_all(yaml_file)
  for yaml_record_set in yaml_record_sets:
    rdata_type = rdatatype.from_text(yaml_record_set['type'])
    if rdata_type not in _RDATA_TRANSLATIONS:
      continue

    record_set = messages.ResourceRecordSet()
    # Need to assign kind to default value for useful equals comparisons.
    record_set.kind = record_set.kind
    record_set.name = yaml_record_set['name']
    record_set.ttl = yaml_record_set['ttl']
    record_set.type = yaml_record_set['type']
    record_set.rrdatas = yaml_record_set['rrdatas']

    if rdata_type is rdatatype.SOA:
      # Make master NS name substitutable.
      rdata_parts = record_set.rrdatas[0].split()
      rdata_parts[0] = '{0}'
      record_set.rrdatas[0] = ' '.join(rdata_parts)
    elif rdata_type is rdatatype.SPF or rdata_type is rdatatype.TXT:
      # Escape text strings to prevent tokenization by the service
      record_set.rrdatas = [_EscapedText(x) for x in record_set.rrdatas]

    record_sets[(record_set.name, record_set.type)] = record_set

  return record_sets


def _RecordSetCopy(record_set):
  """Returns a copy of the given record-set.

  Args:
    record_set: ResourceRecordSet, Record-set to be copied.

  Returns:
    Returns a copy of the given record-set.
  """
  copy = messages.ResourceRecordSet()
  copy.kind = record_set.kind
  copy.name = record_set.name
  copy.type = record_set.type
  copy.ttl = record_set.ttl
  copy.rrdatas = list(record_set.rrdatas)
  return copy


def _SOAReplacement(current_record, record_to_be_imported):
  """Returns the replacement SOA record with restored master NS name.

  Args:
    current_record: ResourceRecordSet, Current record-set.
    record_to_be_imported: ResourceRecordSet, Record-set to be imported.

  Returns:
    ResourceRecordSet, the replacement SOA record with restored master NS name.
  """
  replacement = _RecordSetCopy(record_to_be_imported)
  replacement.rrdatas[0] = replacement.rrdatas[0].format(
      current_record.rrdatas[0].split()[0])

  if replacement == current_record:
    # There should always be a different 'next' SOA record.
    return _NextSOARecordSet(replacement)
  else:
    return replacement


def _RDataReplacement(current_record, record_to_be_imported):
  """Returns a record-set containing rrdata to be imported.

  Args:
    current_record: ResourceRecordSet, Current record-set.
    record_to_be_imported: ResourceRecordSet, Record-set to be imported.

  Returns:
    ResourceRecordSet, a record-set containing rrdata to be imported.
    None, if rrdata to be imported is identical to current rrdata.
  """
  replacement = _RecordSetCopy(record_to_be_imported)
  if replacement == current_record:
    return None
  else:
    return replacement


# Map of functions for replacing rdata of a record-set with rdata from another
# record-set with the same name and type.
_RDATA_REPLACEMENTS = {
    rdatatype.A: _RDataReplacement,
    rdatatype.AAAA: _RDataReplacement,
    rdatatype.CNAME: _RDataReplacement,
    rdatatype.MX: _RDataReplacement,
    rdatatype.PTR: _RDataReplacement,
    rdatatype.SOA: _SOAReplacement,
    rdatatype.SPF: _RDataReplacement,
    rdatatype.SRV: _RDataReplacement,
    rdatatype.TXT: _RDataReplacement,
}


def _NextSOARecordSet(soa_record_set):
  """Returns a new SOA record set with an incremented serial number.

  Args:
    soa_record_set: ResourceRecordSet, Current SOA record-set.

  Returns:
    A a new SOA record-set with an incremented serial number.
  """
  next_soa_record_set = _RecordSetCopy(soa_record_set)
  rdata_parts = soa_record_set.rrdatas[0].split()
  # Increment the 32 bit serial number by one and wrap around if needed.
  rdata_parts[2] = str((long(rdata_parts[2]) + 1) % (1L << 32))
  next_soa_record_set.rrdatas[0] = ' '.join(rdata_parts)
  return next_soa_record_set


def _NameAndType(record):
  return '{0} {1}'.format(record.name, record.type)


def ComputeChange(current, to_be_imported, replace_all=False):
  """Returns a change for importing the given record-sets.

  Args:
    current: dict, (name, type) keyed dict of current record-sets.
    to_be_imported: dict, (name, type) keyed dict of record-sets to be imported.
    replace_all: bool, Whether the record-sets to be imported should replace the
      current record-sets.

  Raises:
    ToolException: If conflicting CNAME records are found.

  Returns:
    A Change that describes the actions required to import the given
    record-sets.
  """
  change = messages.Change()
  change.additions = []
  change.deletions = []

  current_keys = set(current.keys())
  keys_to_be_imported = set(to_be_imported.keys())

  intersecting_keys = current_keys.intersection(keys_to_be_imported)
  if not replace_all and intersecting_keys:
    raise exceptions.ToolException(
        'Conflicting records for the following (name type): {0}'.format(
            [_NameAndType(current[key]) for key in sorted(intersecting_keys)]))

  for key in intersecting_keys:
    current_record = current[key]
    record_to_be_imported = to_be_imported[key]
    rdtype = rdatatype.from_text(key[1])
    replacement = _RDATA_REPLACEMENTS[rdtype](
        current_record, record_to_be_imported)
    if replacement:
      change.deletions.append(current_record)
      change.additions.append(replacement)

  for key in keys_to_be_imported.difference(current_keys):
    change.additions.append(to_be_imported[key])

  for key in current_keys.difference(keys_to_be_imported):
    current_record = current[key]
    rdtype = rdatatype.from_text(key[1])
    if rdtype is rdatatype.SOA:
      change.deletions.append(current_record)
      change.additions.append(_NextSOARecordSet(current_record))
    elif replace_all and rdtype is not rdatatype.NS:
      change.deletions.append(current_record)

  # If the only change is an SOA increment, there is nothing to be done.
  if (len(change.additions) == len(change.deletions) == 1 and
      rdatatype.from_text(change.deletions[0].type) is rdatatype.SOA and
      _NextSOARecordSet(change.deletions[0]) == change.additions[0]):
    return None

  change.additions.sort(key=_NameAndType)
  change.deletions.sort(key=_NameAndType)
  return change
