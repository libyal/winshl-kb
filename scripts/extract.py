#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to extract Windows shell information."""

import argparse
import logging
import os
import sys
import yaml

from dfvfs.helpers import command_line as dfvfs_command_line
from dfvfs.helpers import volume_scanner as dfvfs_volume_scanner
from dfvfs.lib import errors as dfvfs_errors

import winshlrc

from winshlrc import extractor
from winshlrc import yaml_definitions_file


def Main():
  """Entry point of console script to extract Windows shell information.

  Returns:
    int: exit code that is provided to sys.exit().
  """
  argument_parser = argparse.ArgumentParser(description=(
      'Extract Windows shell information.'))

  argument_parser.add_argument(
      '-d', '--debug', dest='debug', action='store_true', default=False,
      help='enable debug output.')

  argument_parser.add_argument(
      '-w', '--windows_version', '--windows-version',
      dest='windows_version', action='store', metavar='Windows XP',
      default=None, help='string that identifies the Windows version.')

  argument_parser.add_argument(
      'source', nargs='?', action='store', metavar='PATH', default=None, help=(
          'path of the volume containing C:\\Windows or the filename of '
          'a storage media image containing the C:\\Windows directory.'))

  options = argument_parser.parse_args()

  if not options.source:
    print('Source value is missing.')
    print('')
    argument_parser.print_help()
    print('')
    return 1

  try:
    with open(options.source, 'r', encoding='utf-8') as file_object:
      source_definitions = list(yaml.safe_load_all(file_object))

  except (SyntaxError, UnicodeDecodeError):
    source_definitions = [{
        'source': options.source, 'windows_version': options.windows_version}]

  logging.basicConfig(
      level=logging.INFO, format='[%(levelname)s] %(message)s')

  data_path = os.path.join(os.path.dirname(winshlrc.__file__), 'data')

  path = os.path.join(data_path, 'observed_shellfolders.yaml')

  definitions_file = yaml_definitions_file.YAMLShellFoldersDefinitionsFile()
  observed_shellfolders = {
      definition.identifier: definition
      for definition in definitions_file.ReadFromFile(path)}

  mediator = dfvfs_command_line.CLIVolumeScannerMediator()

  volume_scanner_options = dfvfs_volume_scanner.VolumeScannerOptions()
  volume_scanner_options.partitions = ['all']
  volume_scanner_options.snapshots = ['none']
  volume_scanner_options.volumes = ['none']

  shell_folder_per_identifier = {}
  windows_versions_per_shell_folder = {}

  for source_definition in source_definitions:
    source_path = source_definition['source']
    logging.info(f'Processing: {source_path:s}')

    extractor_object = extractor.WindowsShellExtractor(
        debug=options.debug, mediator=mediator)

    try:
      result = extractor_object.ScanForWindowsVolume(
          source_path, options=volume_scanner_options)
    except dfvfs_errors.ScannerError:
      result = False

    if not result:
      print((f'Unable to retrieve the volume with the Windows directory '
             f'from: {source_path:s}.'))
      print('')
      return 1

    if extractor_object.windows_version:
      windows_version = extractor_object.windows_version
      logging.info(f'Detected Windows version: {windows_version:s}')

      if source_definition['windows_version']:
        windows_version = source_definition['windows_version']

    else:
      print('Unable to determine Windows version.')

      windows_version = source_definition['windows_version']

    for shell_folder in extractor_object.CollectShellFolders():
      # TODO: compare existing shell folder
      # TODO: track multiple names
      existing_shell_folder = shell_folder_per_identifier.get(
          shell_folder.identifier, None)

      if not existing_shell_folder:
        shell_folder_per_identifier[shell_folder.identifier] = shell_folder
      else:
        if not existing_shell_folder.name:
          existing_shell_folder.name = shell_folder.name
        elif (shell_folder.name and
              shell_folder.name != existing_shell_folder.name and
              shell_folder.name not in existing_shell_folder.alternate_names):
          existing_shell_folder.alternate_names.append(shell_folder.name)

      # TODO: escape \ in name
      # TODO: resolve MUI redirected shell_folder.name

      if shell_folder.identifier not in windows_versions_per_shell_folder:
        windows_versions_per_shell_folder[shell_folder.identifier] = []

      if windows_version:
        windows_versions_per_shell_folder[shell_folder.identifier].append(
            windows_version)

  if not shell_folder_per_identifier:
    print('No shell folder identifiers found.')
    return 0

  # TODO: print new or changed definitions.
  _ = observed_shellfolders

  for identifier, windows_versions in sorted(
      windows_versions_per_shell_folder.items()):
    _ = windows_versions
    shell_folder = shell_folder_per_identifier[identifier]
    print(identifier)

  return 0


if __name__ == '__main__':
  sys.exit(Main())
