#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to generate Windows shell documentation."""

import argparse
import logging
import os
import sys

import winshlrc

from winshlrc import versions
from winshlrc import yaml_definitions_file


class ControlPanelItemsIndexRstOutputWriter(object):
  """Control panel items folder Index.rst output writer."""

  def __init__(self, path):
    """Initializes a control panel items index.rst output writer."""
    super(ControlPanelItemsIndexRstOutputWriter, self).__init__()
    self._file_object = None
    self._path = path

  def __enter__(self):
    """Make this work with the 'with' statement."""
    self._file_object = open(self._path, 'w', encoding='utf-8')

    text = '\n'.join([
        '###################',
        'Control Panel Items',
        '###################',
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

  def WriteControlPanelItem(self, control_panel_item_identifier):
    """Writes a control panel item to the index.rst file.

    Args:
      control_panel_item_identifier (str): control panel item identifier.
    """
    self._file_object.write((
        f'   {control_panel_item_identifier:s} '
        f'<{control_panel_item_identifier:s}>\n'))


class ControlPanelItemMarkdownOutputWriter(object):
  """Control panel item Markdown output writer."""

  _WINDOWS_VERSIONS_KEY_FUNCTION = versions.WindowsVersions.KeyFunction

  def __init__(self, path):
    """Initializes a control panel item Markdown output writer."""
    super(ControlPanelItemMarkdownOutputWriter, self).__init__()
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

  def WriteControlPanelItem(self, control_panel_item_definition):
    """Writes a control panel item to a Markdown file.

    Args:
      control_panel_item_definition (ControlPanelItemDefinition): control panel
          item definition.
    """
    lines = [
        f'## {control_panel_item_definition.identifier:s}',
        '']

    if control_panel_item_definition.windows_versions:
      versions_per_prefix = {}
      for version in sorted(control_panel_item_definition.windows_versions):
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

    module_name = control_panel_item_definition.module_name or '&nbsp;'
    name = control_panel_item_definition.name or '&nbsp;'

    lines.extend([
        '    <tr>',
        '      <td><b>Module name:</b></td>',
        f'      <td>{module_name:s}</td>',
        '    </tr>',
        '    <tr>',
        '      <td><b>Name:</b></td>',
        f'      <td>{name:s}</td>',
        '    </tr>'])

    lines.extend([
        '  </tbody>',
        '</table>',
        '',
        ''])

    text = '\n'.join(lines)
    self._file_object.write(text)


class ShellFoldersIndexRstOutputWriter(object):
  """Shell folders Index.rst output writer."""

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

  def WriteShellFolder(self, shell_folder_identifier):
    """Writes a shell folder to the index.rst file.

    Args:
      shell_folder_identifier (str): shell folder identifier.
    """
    self._file_object.write(
        f'   {shell_folder_identifier:s} <{shell_folder_identifier:s}>\n')


class ShellFolderMarkdownOutputWriter(object):
  """Shell folder Markdown output writer."""

  _WINDOWS_VERSIONS_KEY_FUNCTION = versions.WindowsVersions.KeyFunction

  def __init__(self, path):
    """Initializes a shell folder Markdown output writer."""
    super(ShellFolderMarkdownOutputWriter, self).__init__()
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

  argument_parser.parse_args()

  logging.basicConfig(
      level=logging.INFO, format='[%(levelname)s] %(message)s')

  data_path = os.path.join(os.path.dirname(winshlrc.__file__), 'data')

  definitions_file = (
      yaml_definitions_file.YAMLControlPanelItemsDefinitionsFile())

  control_panel_items = {}

  path = os.path.join(data_path, 'observed_controlpanel_items.yaml')
  for control_panel_item_definition in definitions_file.ReadFromFile(path):
    # TODO: merge observed control panel items with defined control panel items.
    control_panel_items[control_panel_item_definition.identifier] = (
        control_panel_item_definition)

  output_directory = os.path.join('docs', 'sources', 'control-panel-items')
  os.makedirs(output_directory, exist_ok=True)

  index_rst_file_path = os.path.join(output_directory, 'index.rst')
  with ControlPanelItemsIndexRstOutputWriter(
      index_rst_file_path) as index_rst_writer:
    for identifier, control_panel_item_definition in sorted(
        control_panel_items.items()):
      index_rst_writer.WriteControlPanelItem(identifier)

      markdown_file_path = os.path.join(output_directory, f'{identifier:s}.md')
      with ControlPanelItemMarkdownOutputWriter(
          markdown_file_path) as markdown_writer:
        markdown_writer.WriteControlPanelItem(control_panel_item_definition)

  definitions_file = yaml_definitions_file.YAMLShellFoldersDefinitionsFile()

  shell_folders = {}

  path = os.path.join(data_path, 'observed_shellfolders.yaml')
  for shell_folder_definition in definitions_file.ReadFromFile(path):
    shell_folders[shell_folder_definition.identifier] = shell_folder_definition

  output_directory = os.path.join('docs', 'sources', 'shell-folders')
  os.makedirs(output_directory, exist_ok=True)

  index_rst_file_path = os.path.join(output_directory, 'index.rst')
  with ShellFoldersIndexRstOutputWriter(
      index_rst_file_path) as index_rst_writer:
    for identifier, shell_folder_definition in sorted(shell_folders.items()):
      index_rst_writer.WriteShellFolder(identifier)

      markdown_file_path = os.path.join(output_directory, f'{identifier:s}.md')
      with ShellFolderMarkdownOutputWriter(
          markdown_file_path) as markdown_writer:
        markdown_writer.WriteShellFolder(shell_folder_definition)

  return 0


if __name__ == '__main__':
  sys.exit(Main())
