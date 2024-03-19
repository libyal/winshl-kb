#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the YAML-based Windows shell definitions files."""

import unittest

from winshlrc import yaml_definitions_file

from tests import test_lib


class YAMLControlPanelItemsDefinitionsFileTest(test_lib.BaseTestCase):
  """Tests for the YAML-based control panel item definitions file."""

  # pylint: disable=protected-access

  _TEST_YAML = {
      'identifier': 'c58c4893-3be0-4b45-abb5-a63e4b8c8651',
      'module_name': 'Troubleshooting',
      'name': 'Microsoft.Troubleshooting',
      'windows_versions': ['Windows XP 32-bit', 'Windows 10 (1511)']}

  def testReadControlPanelItemDefinition(self):
    """Tests the _ReadControlPanelItemDefinition function."""
    test_definitions_file = (
        yaml_definitions_file.YAMLControlPanelItemsDefinitionsFile())

    definitions = test_definitions_file._ReadControlPanelItemDefinition(
        self._TEST_YAML)

    self.assertIsNotNone(definitions)
    self.assertEqual(
        definitions.identifier, 'c58c4893-3be0-4b45-abb5-a63e4b8c8651')
    self.assertEqual(definitions.module_name, 'Troubleshooting')
    self.assertEqual(definitions.name, 'Microsoft.Troubleshooting')
    self.assertEqual(
        definitions.windows_versions,
        ['Windows XP 32-bit', 'Windows 10 (1511)'])

    with self.assertRaises(RuntimeError):
      test_definitions_file._ReadControlPanelItemDefinition({})

    with self.assertRaises(RuntimeError):
      test_definitions_file._ReadControlPanelItemDefinition({
          'module_name': 'Troubleshooting',
          'name': 'Microsoft.Troubleshooting',
          'windows_versions': ['Windows XP 32-bit', 'Windows 10 (1511)']})

    with self.assertRaises(RuntimeError):
      test_definitions_file._ReadControlPanelItemDefinition({
          'bogus': 'test'})

  def testReadFromFileObject(self):
    """Tests the _ReadFromFileObject function."""
    test_file_path = self._GetTestFilePath(['controlpanel_items.yaml'])
    self._SkipIfPathNotExists(test_file_path)

    test_definitions_file = (
        yaml_definitions_file.YAMLControlPanelItemsDefinitionsFile())

    with open(test_file_path, 'r', encoding='utf-8') as file_object:
      definitions = list(test_definitions_file._ReadFromFileObject(file_object))

    self.assertEqual(len(definitions), 4)

  def testReadFromFile(self):
    """Tests the ReadFromFile function."""
    test_file_path = self._GetTestFilePath(['controlpanel_items.yaml'])
    self._SkipIfPathNotExists(test_file_path)

    test_definitions_file = (
        yaml_definitions_file.YAMLControlPanelItemsDefinitionsFile())

    definitions = list(test_definitions_file.ReadFromFile(test_file_path))

    self.assertEqual(len(definitions), 4)

    self.assertEqual(
        definitions[0].identifier, '78cb147a-98ea-4aa6-b0df-c8681f69341c')
    self.assertEqual(
        definitions[3].identifier, 'fcfeecae-ee1b-4849-ae50-685dcf7717ec')


class YAMLKnownFoldersDefinitionsFileTest(test_lib.BaseTestCase):
  """Tests for the YAML-based known folder definitions file."""

  # pylint: disable=protected-access

  _TEST_YAML = {
      'identifier': '0762d272-c50a-4bb0-a382-697dcd729b80',
      'name': 'UserProfiles',
      'windows_versions': ['Windows XP 32-bit', 'Windows 10 (1511)']}

  def testReadKnownFolderDefinition(self):
    """Tests the _ReadKnownFolderDefinition function."""
    test_definitions_file = (
        yaml_definitions_file.YAMLKnownFoldersDefinitionsFile())

    definitions = test_definitions_file._ReadKnownFolderDefinition(
        self._TEST_YAML)

    self.assertIsNotNone(definitions)
    self.assertEqual(
        definitions.identifier, '0762d272-c50a-4bb0-a382-697dcd729b80')
    self.assertEqual(definitions.name, 'UserProfiles')
    self.assertEqual(
        definitions.windows_versions,
        ['Windows XP 32-bit', 'Windows 10 (1511)'])

    with self.assertRaises(RuntimeError):
      test_definitions_file._ReadKnownFolderDefinition({})

    with self.assertRaises(RuntimeError):
      test_definitions_file._ReadKnownFolderDefinition({
          'name': 'UserProfiles',
          'windows_versions': ['Windows XP 32-bit', 'Windows 10 (1511)']})

    with self.assertRaises(RuntimeError):
      test_definitions_file._ReadKnownFolderDefinition({
          'bogus': 'test'})

  def testReadFromFileObject(self):
    """Tests the _ReadFromFileObject function."""
    test_file_path = self._GetTestFilePath(['knownfolders.yaml'])
    self._SkipIfPathNotExists(test_file_path)

    test_definitions_file = (
        yaml_definitions_file.YAMLKnownFoldersDefinitionsFile())

    with open(test_file_path, 'r', encoding='utf-8') as file_object:
      definitions = list(test_definitions_file._ReadFromFileObject(file_object))

    self.assertEqual(len(definitions), 2)

  def testReadFromFile(self):
    """Tests the ReadFromFile function."""
    test_file_path = self._GetTestFilePath(['knownfolders.yaml'])
    self._SkipIfPathNotExists(test_file_path)

    test_definitions_file = (
        yaml_definitions_file.YAMLKnownFoldersDefinitionsFile())

    definitions = list(test_definitions_file.ReadFromFile(test_file_path))

    self.assertEqual(len(definitions), 2)

    self.assertEqual(
        definitions[0].identifier, '1c2ac1dc-4358-4b6c-9733-af21156576f0')
    self.assertEqual(
        definitions[1].identifier, '2f8b40c2-83ed-48ee-b383-a1f157ec6f9a')


class YAMLShellFoldersDefinitionsFileTest(test_lib.BaseTestCase):
  """Tests for the YAML-based shell folder definitions file."""

  # pylint: disable=protected-access

  _TEST_YAML = {
      'identifier': '20d04fe0-3aea-1069-a2d8-08002b30309d',
      'name': 'My Computer',
      'alternate_names': ['Computer', 'This PC'],
      'windows_versions': ['Windows XP 32-bit', 'Windows 10 (1511)']}

  def testReadShellFolderDefinition(self):
    """Tests the _ReadShellFolderDefinition function."""
    test_definitions_file = (
        yaml_definitions_file.YAMLShellFoldersDefinitionsFile())

    definitions = test_definitions_file._ReadShellFolderDefinition(
        self._TEST_YAML)

    self.assertIsNotNone(definitions)
    self.assertEqual(
        definitions.identifier, '20d04fe0-3aea-1069-a2d8-08002b30309d')
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
        definitions[0].identifier, '0afaced1-e828-11d1-9187-b532f1e9575d')
    self.assertEqual(
        definitions[2].identifier, '7a9d77bd-5403-11d2-8785-2e0420524153')


if __name__ == '__main__':
  unittest.main()
