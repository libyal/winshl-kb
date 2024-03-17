#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to generate Windows shell documentation."""

import argparse
import logging
import os
import sys
import yaml

from winshlrc import versions


class MarkdownOutputWriter(object):
  """Markdown output writer."""

  _WINDOWS_VERSIONS_KEY_FUNCTION = versions.WindowsVersions.KeyFunction

  def __init__(self, path):
    """Initializes a Markdown output writer."""
    super(MarkdownOutputWriter, self).__init__()
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

  def WriteShellFolder(self, shell_folder):
    """Writes a shell folder to a Markdown file.

    Args:
      shell_folder (dict): shell folder.
    """
    lines = []

    identifier = shell_folder.get('identifier', None)
    lines.extend([
        '<table border="1" class="docutils">',
        '  <tbody>',
        '    <tr>',
        '      <td><b>Identifier:</b></td>',
        f'      <td>{identifier:s}</td>',
        '    </tr>'])

    name = shell_folder.get('name', None)
    if name:
      lines.extend([
          '    <tr>',
          '      <td><b>Name:</b></td>',
          f'      <td>{name:s}</td>',
          '    </tr>'])

    class_name = shell_folder.get('class_name', None)
    if class_name:
      lines.extend([
          '    <tr>',
          '      <td><b>Class name:</b></td>',
          f'      <td>{class_name:s}</td>',
          '    </tr>'])

    windows_versions = shell_folder.get('windows_versions', None)
    if windows_versions:
      # TODO: combine Windows versions into a more compact string
      versions_per_prefix = {}
      for version in sorted(windows_versions):
        for prefix in ('Windows 10', 'Windows 11', None):
          if prefix and version.startswith(prefix):
            break

        if not prefix:
          versions_per_prefix[version] = []
        else:
          if prefix not in versions_per_prefix:
            versions_per_prefix[prefix] = []
          versions_per_prefix[prefix].append(version[len(prefix) + 2:-1])

      version_strings = []
      for prefix, sub_versions in sorted(
          versions_per_prefix.items(),
          key=lambda item: self._WINDOWS_VERSIONS_KEY_FUNCTION(item[0])):
        if not sub_versions:
          version_string = prefix
        else:
          sub_versions_string = ', '.join(sub_versions)
          version_string = f'{prefix:s} ({sub_versions_string:s})'

        version_strings.append(version_string)

      version_strings = ', '.join(version_strings)
      lines.extend([
          '    <tr>',
          '      <td><b>Seen on:</b></td>',
          f'      <td>{version_strings:s}</td>',
          '    </tr>'])

    lines.extend([
        '  </tbody>',
        '</table>',
        '',
        '&nbsp;',
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

  argument_parser.parse_args()

  logging.basicConfig(
      level=logging.INFO, format='[%(levelname)s] %(message)s')

  data_path = os.getcwd()
  data_file = os.path.join(data_path, 'shellfolders.yaml')

  try:
    with open(data_file, 'r', encoding='utf-8') as file_object:
      shell_folders = list(yaml.safe_load_all(file_object))

  except (SyntaxError, UnicodeDecodeError) as exception:
    print(f'Unable to read shellfolders.yaml with error: {exception!s}')
    return 0

  with MarkdownOutputWriter('test.md') as markdown_writer:
   for shell_folder in shell_folders:
     markdown_writer.WriteShellFolder(shell_folder)

  return 0


if __name__ == '__main__':
  sys.exit(Main())
