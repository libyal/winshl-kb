#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to combine winshl-kb YAML files."""

import argparse
import glob
import os
import sys
import uuid
import yaml

from winshlrc import resources


class YAMLOutputWriter(object):
  """YAML output writer."""

  def __enter__(self):
    """Make this work with the 'with' statement."""
    return self

  def __exit__(self, exception_type, value, traceback):
    """Make this work with the 'with' statement."""

  def WriteKnownFolder(self, known_folder_definition):
    """Writes a known folder definition in YAML to stdout.

    Args:
      known_folder_definition (KnownFolderDefinition): known folder definition.
    """
    print('---')

    if known_folder_definition.name:
      print(f'name: {known_folder_definition.name:s}')

    print(f'identifier: {known_folder_definition.identifier:s}')

    if known_folder_definition.display_name:
      print(f'display_name: "{known_folder_definition.display_name:s}"')

    if known_folder_definition.default_path:
      default_path = known_folder_definition.default_path.replace('\\', '\\\\')
      print(f'default_path: "{default_path:s}"')

    if known_folder_definition.csidl:
      csidl = ', '.join(known_folder_definition.csidl)
      print(f'csidl: [{csidl:s}]')

    if known_folder_definition.legacy_display_name:
      print((f'legacy_display_name: '
             f'"{known_folder_definition.legacy_display_name:s}"'))

    if known_folder_definition.legacy_default_path:
      legacy_default_path = known_folder_definition.legacy_default_path.replace(
          '\\', '\\\\')
      print(f'legacy_default_path: "{legacy_default_path:s}"')


def Main():
  """Entry point of console script to combine winshl-kb YAML files.

  Returns:
    int: exit code that is provided to sys.exit().
  """
  argument_parser = argparse.ArgumentParser(description=(
      'Merges winshl-kb YAML files.'))

  argument_parser.add_argument(
      'source', nargs='?', action='store', metavar='PATH',
      default=None, help='path of a directory with winshl-kb YAML files.')

  options = argument_parser.parse_args()

  if not options.source:
    print('Source directory missing.')
    print('')
    argument_parser.print_help()
    print('')
    return 1

  known_folder_definitions = {}

  for path in glob.glob(os.path.join(options.source, '*.yaml')):
    with open(path, 'r', encoding='utf8') as file_object:
      for yaml_definition in yaml.safe_load_all(file_object):
        csidl = yaml_definition.get('csidl', None)
        display_name = yaml_definition.get('display_name', None)
        default_path = yaml_definition.get('default_path', None)
        legacy_display_name = yaml_definition.get('legacy_display_name', None)
        legacy_default_path = yaml_definition.get('legacy_default_path', None)
        name = yaml_definition.get('name', None)
        identifier = yaml_definition.get('identifier', None)

        # Test if the identifier is a GUID value.
        _ = uuid.UUID(identifier)

        known_folder_definition = known_folder_definitions.get(identifier, None)
        if not known_folder_definition:
          known_folder_definition = resources.KnownFolderDefinition()
          known_folder_definition.identifier = identifier

          known_folder_definitions[identifier] = known_folder_definition

        if csidl and not known_folder_definition.display_name:
          known_folder_definition.csidl = csidl
        if display_name and not known_folder_definition.display_name:
          known_folder_definition.display_name = display_name
        if default_path and not known_folder_definition.default_path:
          known_folder_definition.default_path = default_path
        if (legacy_display_name and
            not known_folder_definition.legacy_display_name):
          known_folder_definition.legacy_display_name = legacy_display_name
        if (legacy_default_path and
            not known_folder_definition.legacy_default_path):
          known_folder_definition.legacy_default_path = legacy_default_path
        if name and not known_folder_definition.name:
          known_folder_definition.name = name

  with YAMLOutputWriter() as yaml_writer:
    for known_folder_definition in sorted(
        known_folder_definitions.values(),
        key=lambda definition: definition.identifier):
      yaml_writer.WriteKnownFolder(known_folder_definition)

  return 0


if __name__ == '__main__':
  sys.exit(Main())
