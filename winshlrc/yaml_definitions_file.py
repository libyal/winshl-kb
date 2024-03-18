# -*- coding: utf-8 -*-
"""YAML-based Windows shell definitions files."""

import yaml

from winshlrc import resources


class YAMLControlPanelItemsDefinitionsFile(object):
  """YAML-based control panel item definitions file.

  A YAML-based control panel item definitions file contains one or more control
  panel item definitions. A control panel item definition consists of:

  identifier: c58c4893-3be0-4b45-abb5-a63e4b8c8651
  module_name: "Troubleshooting"
  name: "Microsoft.Troubleshooting"
  windows_versions: ["Windows XP 32-bit", "Windows 10 (1511)"]

  Where:
  * identifier, defines the control panel item identifier;
  * module_name, defines the module name of the control panel item;
  * name, defines the name of the control panel item;
  * windows_versions, defines Windows versions the control panel item was seen.
  """

  _SUPPORTED_KEYS = frozenset([
      'identifier',
      'module_name',
      'name',
      'windows_versions'])

  def _ReadControlPanelItemDefinition(self, yaml_control_panel_item_definition):
    """Reads a control panel item definition from a dictionary.

    Args:
      yaml_control_panel_item_definition (dict[str, object]): YAML control panel
          item definition values.

    Returns:
      ControlPanelItemDefinition: control panel item definition.

    Raises:
      RuntimeError: if the format of the formatter definition is not set
          or incorrect.
    """
    if not yaml_control_panel_item_definition:
      raise RuntimeError('Missing control panel item definition values.')

    different_keys = set(
        yaml_control_panel_item_definition) - self._SUPPORTED_KEYS
    if different_keys:
      different_keys = ', '.join(different_keys)
      raise RuntimeError('Undefined keys: {0:s}'.format(different_keys))

    identifier = yaml_control_panel_item_definition.get('identifier', None)
    if not identifier:
      raise RuntimeError(
          'Invalid control panel item definition missing identifier.')

    control_panel_item_definition = resources.ControlPanelItemDefinition()
    control_panel_item_definition.identifier = identifier
    control_panel_item_definition.module_name = (
        yaml_control_panel_item_definition.get('module_name', None))
    control_panel_item_definition.name = (
        yaml_control_panel_item_definition.get('name', None))
    control_panel_item_definition.windows_versions = (
        yaml_control_panel_item_definition.get('windows_versions', []))

    return control_panel_item_definition

  def _ReadFromFileObject(self, file_object):
    """Reads the event formatters from a file-like object.

    Args:
      file_object (file): formatters file-like object.

    Yields:
      ControlPanelItemDefinition: control panel item definition.
    """
    yaml_generator = yaml.safe_load_all(file_object)

    for yaml_control_panel_item_definition in yaml_generator:
      yield self._ReadControlPanelItemDefinition(
          yaml_control_panel_item_definition)

  def ReadFromFile(self, path):
    """Reads the event formatters from a YAML file.

    Args:
      path (str): path to a formatters file.

    Yields:
      ControlPanelItemDefinition: control panel item definition.
    """
    with open(path, 'r', encoding='utf-8') as file_object:
      for yaml_control_panel_item_definition in self._ReadFromFileObject(
          file_object):
        yield yaml_control_panel_item_definition


class YAMLShellFoldersDefinitionsFile(object):
  """YAML-based shell folders definitions file.

  A YAML-based shell folders definitions file contains one or more shell folder
  definitions. A shell folder definition consists of:

  identifier: 20d04fe0-3aea-1069-a2d8-08002b30309d
  name: "My Computer"
  alternate_names: ["Computer", "This PC"]
  windows_versions: ["Windows XP 32-bit", "Windows 10 (1511)"]

  Where:
  * alternate_names, defines alternate names of the shell folder;
  * class_name, defines the name of the shell folder class;
  * identifier, defines the shell folder identifier;
  * name, defines the name of the shell folder;
  * windows_versions, defines Windows versions the shell folder was seen.
  """

  _SUPPORTED_KEYS = frozenset([
      'alternate_names',
      'class_name',
      'identifier',
      'name',
      'windows_versions'])

  def _ReadShellFolderDefinition(self, yaml_shell_folder_definition):
    """Reads a shell folder definition from a dictionary.

    Args:
      yaml_shell_folder_definition (dict[str, object]): YAML shell folder
          definition values.

    Returns:
      ShellFolderDefinition: shell folder definition.

    Raises:
      RuntimeError: if the format of the formatter definition is not set
          or incorrect.
    """
    if not yaml_shell_folder_definition:
      raise RuntimeError('Missing shell folder definition values.')

    different_keys = set(yaml_shell_folder_definition) - self._SUPPORTED_KEYS
    if different_keys:
      different_keys = ', '.join(different_keys)
      raise RuntimeError('Undefined keys: {0:s}'.format(different_keys))

    identifier = yaml_shell_folder_definition.get('identifier', None)
    if not identifier:
      raise RuntimeError('Invalid shell folder definition missing identifier.')

    shell_folder_definition = resources.ShellFolderDefinition()
    shell_folder_definition.alternate_names = (
        yaml_shell_folder_definition.get('alternate_names', []))
    shell_folder_definition.class_name = (
        yaml_shell_folder_definition.get('class_name', None))
    shell_folder_definition.identifier = identifier
    shell_folder_definition.name = (
        yaml_shell_folder_definition.get('name', None))
    shell_folder_definition.windows_versions = (
        yaml_shell_folder_definition.get('windows_versions', []))

    return shell_folder_definition

  def _ReadFromFileObject(self, file_object):
    """Reads the event formatters from a file-like object.

    Args:
      file_object (file): formatters file-like object.

    Yields:
      ShellFolderDefinition: shell folder definition.
    """
    yaml_generator = yaml.safe_load_all(file_object)

    for yaml_shell_folder_definition in yaml_generator:
      yield self._ReadShellFolderDefinition(yaml_shell_folder_definition)

  def ReadFromFile(self, path):
    """Reads the event formatters from a YAML file.

    Args:
      path (str): path to a formatters file.

    Yields:
      ShellFolderDefinition: shell folder definition.
    """
    with open(path, 'r', encoding='utf-8') as file_object:
      for yaml_shell_folder_definition in self._ReadFromFileObject(file_object):
        yield yaml_shell_folder_definition
