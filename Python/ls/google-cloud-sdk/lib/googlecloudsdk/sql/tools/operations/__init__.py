# Copyright 2013 Google Inc. All Rights Reserved.

"""Provide commands for working with Cloud SQL instance operations."""

from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions


class Operations(base.Group):
  """Provide commands for working with Cloud SQL instance operations.

  Provide commands for working with Cloud SQL instance operations, including
  listing and getting information about instance operations of a Cloud SQL
  instance.
  """

  @staticmethod
  def Args(parser):
    parser.add_argument(
        '--instance',
        '-i',
        help='Cloud SQL instance ID.')

  def Filter(self, tool_context, args):
    if not args.instance:
      raise exceptions.ToolException('argument --instance/-i is required')
