#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the YAML-based Windows shell definitions files."""

import unittest

from winshlrc import yaml_definitions_file

from tests import test_lib


class YAMLShellFoldersDefinitionsFileTest(test_lib.BaseTestCase):
  """Tests for the YAML-based shell folder definitions file."""

  # pylint: disable=protected-access

  _TEST_YAML = {
      'identifier': '{20d04fe0-3aea-1069-a2d8-08002b30309d}',
      'name': 'My Computer',
      'alternate_names': ['Computer', 'This PC'],
      'windows_versions': ['Windows XP 32-bit', 'Windows 10 (1511)']}

  def testReadShellFolderfinition(self):
    """Tests the _ReadShellFolderfinition function."""
    test_definitions_file = (
        yaml_definitions_file.YAMLShellFoldersDefinitionsFile())

    definitions = test_definitions_file._ReadShellFolderDefinition(
        self._TEST_YAML)

    self.assertIsNotNone(definitions)
    self.assertEqual(
        definitions.identifier, '{20d04fe0-3aea-1069-a2d8-08002b30309d}')
    self.assertEqual(definitions.name, 'My Computer')
    self.assertEqual(definitions.alternate_names, ['Computer', 'This PC'])
    self.assertEqual(
        definitions.windows_versions,
        ['Windows XP 32-bit', 'Windows 10 (1511)'])

    with self.assertRaises(RuntimeError):
      test_definitions_file._ReadShellFolderDefinition({})

    with self.assertRaises(RuntimeError):
      test_definitions_file._ReadShellFolderDefinition({
          'name': 'My Computer',
          'alternate_names': ['Computer', 'This PC'],
          'windows_versions': ['Windows XP 32-bit', 'Windows 10 (1511)']})

    with self.assertRaises(RuntimeError):
      test_definitions_file._ReadShellFolderDefinition({
          'bogus': 'test'})

  def testReadFromFileObject(self):
    """Tests the _ReadFromFileObject function."""
    test_file_path = self._GetTestFilePath(['shellfolders.yaml'])
    self._SkipIfPathNotExists(test_file_path)

    test_definitions_file = (
        yaml_definitions_file.YAMLShellFoldersDefinitionsFile())

    with open(test_file_path, 'r', encoding='utf-8') as file_object:
      definitions = list(test_definitions_file._ReadFromFileObject(file_object))

    self.assertEqual(len(definitions), 3)

  def testReadFromFile(self):
    """Tests the ReadFromFile function."""
    test_file_path = self._GetTestFilePath(['shellfolders.yaml'])
    self._SkipIfPathNotExists(test_file_path)

    test_definitions_file = (
        yaml_definitions_file.YAMLShellFoldersDefinitionsFile())

    definitions = list(test_definitions_file.ReadFromFile(test_file_path))

    self.assertEqual(len(definitions), 3)

    self.assertEqual(
        definitions[0].identifier, '{0afaced1-e828-11d1-9187-b532f1e9575d}')
    self.assertEqual(
        definitions[2].identifier, '{7a9d77bd-5403-11d2-8785-2e0420524153}')


if __name__ == '__main__':
  unittest.main()
