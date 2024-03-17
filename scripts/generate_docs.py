#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to generate Windows shell documentation."""

import argparse
import logging
import os
import sys

from winshlrc import versions
from winshlrc import yaml_definitions_file


class ShellFoldersIndexRstOutputWriter(object):
  """Shell folder Index.rst output writer."""

  def __init__(self, path):
    """Initializes a shell folders index.rst output writer."""
    super(ShellFoldersIndexRstOutputWriter, self).__init__()
    self._file_object = None
    self._path = path

  def __enter__(self):
    """Make this work with the 'with' statement."""
    self._file_object = open(self._path, 'w', encoding='utf-8')

    text = '\n'.join([
        '#############',
        'Shell Folders',
        '#############',
        '',
        '.. toctree::',
        '   :maxdepth: 1',
        '',
        ''])
    self._file_object.write(text)

    return self

  def __exit__(self, exception_type, value, traceback):
    """Make this work with the 'with' statement."""
    self._file_object.close()
    self._file_object = None

  def WritePropertySet(self, shell_folder_identifier):
    """Writes a shell folder to the index.rst file.

    Args:
      shell_folder_identifier (str): shell folder identifier.
    """
    self._file_object.write(
        f'   {shell_folder_identifier:s} <{shell_folder_identifier:s}>\n')


class ShellFoldersMarkdownOutputWriter(object):
  """Shell folders Markdown output writer."""

  _WINDOWS_VERSIONS_KEY_FUNCTION = versions.WindowsVersions.KeyFunction

  def __init__(self, path):
    """Initializes a shell folders Markdown output writer."""
    super(ShellFoldersMarkdownOutputWriter, self).__init__()
    self._file_object = None
    self._path = path

  def __enter__(self):
    """Make this work with the 'with' statement."""
    self._file_object = open(self._path, 'w', encoding='utf-8')
    return self

  def __exit__(self, exception_type, value, traceback):
    """Make this work with the 'with' statement."""
    self._file_object.close()
    self._file_object = None

  def WriteShellFolder(self, shell_folder_definition):
    """Writes a shell folder to a Markdown file.

    Args:
      shell_folder_definition (ShellFolderDefinition): shell folder definition.
    """
    lines = [
        f'## {shell_folder_definition.identifier:s}',
        '']

    if shell_folder_definition.windows_versions:
      versions_per_prefix = {}
      for version in sorted(shell_folder_definition.windows_versions):
        for prefix in ('Windows 10', 'Windows 11', None):
          if prefix and version.startswith(prefix):
            break

        if not prefix:
          versions_per_prefix[version] = []
        else:
          if prefix not in versions_per_prefix:
            versions_per_prefix[prefix] = []
          versions_per_prefix[prefix].append(version[len(prefix) + 2:-1])

      lines.append('Seen on:')

      for prefix, sub_versions in sorted(
          versions_per_prefix.items(),
          key=lambda item: self._WINDOWS_VERSIONS_KEY_FUNCTION(item[0])):
        if not sub_versions:
          line = f'* {prefix:s}'
        else:
          sub_versions_string = ', '.join(sub_versions)
          line = f'* {prefix:s} ({sub_versions_string:s})'

        lines.append(line)

      lines.append('')

    lines.extend([
        '<table border="1" class="docutils">',
        '  <tbody>'])

    class_name = shell_folder_definition.class_name or '&nbsp;'
    name = shell_folder_definition.name or '&nbsp;'

    lines.extend([
        '    <tr>',
        '      <td><b>Class name:</b></td>',
        f'      <td>{class_name:s}</td>',
        '    </tr>',
        '    <tr>',
        '      <td><b>Name:</b></td>',
        f'      <td>{name:s}</td>',
        '    </tr>'])

    if shell_folder_definition.alternate_names:
      for index, name in enumerate(shell_folder_definition.alternate_names):
        if index == 0:
          lines.extend([
              '    <tr>',
              '      <td><b>Alternate name(s):</b></td>',
              f'      <td>{name:s}</td>',
              '    </tr>'])
        else:
          lines.extend([
              '    <tr>',
              '      <td>&nbsp;</b></td>',
              f'      <td>{name:s}</td>',
              '    </tr>'])

    lines.extend([
        '  </tbody>',
        '</table>',
        '',
        ''])

    text = '\n'.join(lines)
    self._file_object.write(text)


def Main():
  """Entry point of console script to generate Windows shell documentation.

  Returns:
    int: exit code that is provided to sys.exit().
  """
  argument_parser = argparse.ArgumentParser(description=(
      'Generated Windows shell documentation.'))

  argument_parser.add_argument(
      'source', nargs='?', action='store', metavar='PATH', default=None,
      help='path of the Windows shell related data file.')

  options = argument_parser.parse_args()

  if not options.source:
    print('Source value is missing.')
    print('')
    argument_parser.print_help()
    print('')
    return False

  logging.basicConfig(
      level=logging.INFO, format='[%(levelname)s] %(message)s')

  try:
    with open(options.source, 'r', encoding='utf-8') as file_object:
      data_header = file_object.readline()

  except (SyntaxError, UnicodeDecodeError) as exception:
    print(f'Unable to read data haeader with error: {exception!s}')
    return 0

  if not data_header.startswith('# winshl-kb shellfolder definitions'):
    print('Unsupported data file.')
    print('')
    return 1

  if data_header.startswith('# winshl-kb shellfolder definitions'):
    definitions_file = yaml_definitions_file.YAMLShellFoldersDefinitionsFile()

    output_directory = os.path.join('docs', 'sources', 'shell-folders')
    os.makedirs(output_directory, exist_ok=True)

    index_rst_file_path = os.path.join(output_directory, 'index.rst')
    with ShellFoldersIndexRstOutputWriter(
        index_rst_file_path) as index_rst_writer:
      for shell_folder_definition in definitions_file.ReadFromFile(
          options.source):
        index_rst_writer.WritePropertySet(shell_folder_definition.identifier)

        markdown_file_path = os.path.join(
            output_directory, f'{shell_folder_definition.identifier:s}.md')
        with ShellFoldersMarkdownOutputWriter(
            markdown_file_path) as markdown_writer:
          markdown_writer.WriteShellFolder(shell_folder_definition)

  return 0


if __name__ == '__main__':
  sys.exit(Main())
