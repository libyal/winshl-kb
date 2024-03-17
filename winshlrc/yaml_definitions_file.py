# -*- coding: utf-8 -*-
"""YAML-based Windows shell definitions files."""

import yaml

from winshlrc import resources


class YAMLShellFoldersDefinitionsFile(object):
  """YAML-based shell folders definitions file.

  A YAML-based shell folders definitions file contains one or more shell folder
  definitions. A shell folder definition consists of:

  identifier: {20d04fe0-3aea-1069-a2d8-08002b30309d}
  name: "My Computer"
  alternate_names: ["Computer", "This PC"]
  windows_versions: ["Windows XP 32-bit", "Windows 10 (1511)"]

  Where:
  * alternate_names, defines alternate names of the shell folder;
  * identifier, defines the shell folder identifier;
  * class_name, defines the name of the shell folder class;
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
    shell_folder_definition.alternate_names = yaml_shell_folder_definition.get(
        'alternate_names', [])
    shell_folder_definition.class_name = yaml_shell_folder_definition.get(
        'class_name', None)
    shell_folder_definition.identifier = identifier
    shell_folder_definition.name = yaml_shell_folder_definition.get(
        'name', None)
    shell_folder_definition.windows_versions = yaml_shell_folder_definition.get(
        'windows_versions', [])

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
