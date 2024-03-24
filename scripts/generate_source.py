#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to generate Windows shell related source code."""

import argparse
import logging
import os
import sys
import uuid

import winshlrc

from winshlrc import yaml_definitions_file


class LibfwsiControlPanelItemIdentifierGenerator(object):
  """Generator for libfwsi control_panel_item_identifier.[ch] source code."""

  _C_FILE_HEADER = """\
/*
 * Control panel item identifier functions
 *
 * Copyright (C) 2010-2024, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <common.h>
#include <memory.h>
#include <types.h>

#include "libfwsi_control_panel_item_identifier.h"
#include "libfwsi_libcerror.h"

"""

  _C_FILE_MIDDLE = """\

uint8_t libfwsi_control_panel_item_identifier_unknown[ 16 ] = {
\t0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff };

/* The control panel item identifiers
 */
libfwsi_control_panel_item_identifier_definition_t libfwsi_control_panel_item_identifier_definitions[ ] = {

"""

  _C_FILE_FOOTER = """\

\t{ libfwsi_control_panel_item_identifier_unknown,
\t  "Unknown" } };

/* Retrieves a string containing the name of the folder identifier
 */
const char *libfwsi_control_panel_item_identifier_get_name(
             const uint8_t *control_panel_item_identifier )
{
\tint iterator = 0;

\tif( control_panel_item_identifier == NULL )
\t{
\t\treturn( "Invalid control panel item identifier" );
\t}
\twhile( memory_compare(
\t        ( libfwsi_control_panel_item_identifier_definitions[ iterator ] ).identifier,
\t        libfwsi_control_panel_item_identifier_unknown,
\t        16 ) != 0 )
\t{
\t\tif( memory_compare(
\t\t     ( libfwsi_control_panel_item_identifier_definitions[ iterator ] ).identifier,
\t\t     control_panel_item_identifier,
\t\t     16 ) == 0 )
\t\t{
\t\t\tbreak;
\t\t}
\t\titerator++;
\t}
\treturn(
\t ( libfwsi_control_panel_item_identifier_definitions[ iterator ] ).name );
}

"""

  _H_FILE_HEADER = """\
/*
 * Control panel item identifier functions
 *
 * Copyright (C) 2010-2024, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#if !defined( _LIBFWSI_CONTROL_PANEL_ITEM_IDENTIFIER_H )
#define _LIBFWSI_CONTROL_PANEL_ITEM_IDENTIFIER_H

#include <common.h>
#include <types.h>

#include "libfwsi_extern.h"
#include "libfwsi_libcerror.h"

#if defined( __cplusplus )
extern "C" {
#endif

/* The CLSID is stored as a little endian GUID
 */
typedef struct libfwsi_control_panel_item_identifier_definition libfwsi_control_panel_item_identifier_definition_t;

struct libfwsi_control_panel_item_identifier_definition
{
\t/* The identifier
\t */
\tuint8_t *identifier;

\t/* The name
\t */
\tconst char *name;
};

"""

  _H_FILE_FOOTER = """\

extern uint8_t libfwsi_control_panel_item_identifier_unknown[ 16 ];

LIBFWSI_EXTERN \\
const char *libfwsi_control_panel_item_identifier_get_name(
             const uint8_t *control_panel_item_identifier );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBFWSI_CONTROL_PANEL_ITEM_IDENTIFIER_H ) */

"""

  def __init__(self, path):
    """Initializes a libfwsi control_panel_item_identifier.[ch] generator.

    Args:
      path (str): path.
    """
    super(LibfwsiControlPanelItemIdentifierGenerator, self).__init__()
    self._path = path

  def GenerateCFile(self, control_panel_items):
    """Generates the C source code file.

    Args:
      control_panel_items (dict[str, ControlPanelItemDefinition]): control
          panel item per name.
    """
    output_path = os.path.join(
        self._path, 'libfwsi', 'libfwsi_control_panel_item_identifier.c')
    with open(output_path, 'w', encoding='utf8') as file_object:
      file_object.write(self._C_FILE_HEADER)

      for name, control_panel_item_definition in sorted(
          control_panel_items.items()):
        identifier = uuid.UUID(control_panel_item_definition.identifier)
        byte_values = ', '.join(
            f'0x{byte_value:02x}' for byte_value in identifier.bytes_le)

        file_object.write((
            f'uint8_t libfwsi_control_panel_item_identifier_{name:s}[ 16 ] '
            f'= {{\n'
            f'\t{byte_values:s} }};\n'
            '\n'))

      file_object.write(self._C_FILE_MIDDLE)

      for name, control_panel_item_definition in sorted(
          control_panel_items.items()):
        name_string = control_panel_item_definition.module_name
        file_object.write((
            f'\t{{ libfwsi_control_panel_item_identifier_{name:s},\n'
            f'\t  "{name_string:s}" }},\n'))

      file_object.write(self._C_FILE_FOOTER)

  def GenerateHFile(self, control_panel_items):
    """Generates the H source code file.

    Args:
      control_panel_items (dict[str, ControlPanelItemDefinition]): control
          panel item per name.
    """
    output_path = os.path.join(
        self._path, 'libfwsi', 'libfwsi_control_panel_item_identifier.h')
    with open(output_path, 'w', encoding='utf8') as file_object:
      file_object.write(self._H_FILE_HEADER)

      for name in sorted(control_panel_items):
        file_object.write((
            f'extern uint8_t '
            f'libfwsi_control_panel_item_identifier_{name:s}[ 16 ];\n'))

      file_object.write(self._H_FILE_FOOTER)


class LibfwsiKnownFolderIdentifierGenerator(object):
  """Generator for libfwsi known_folder_identifier.[ch] source code."""

  _C_FILE_HEADER = """\
/*
 * Known folder identifier functions
 *
 * Copyright (C) 2010-2024, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <common.h>
#include <memory.h>
#include <types.h>

#include "libfwsi_known_folder_identifier.h"
#include "libfwsi_libcerror.h"

"""

  _C_FILE_MIDDLE = """\

uint8_t libfwsi_known_folder_identifier_unknown[ 16 ] = {
\t0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff };

/* The known folder identifiers
 */
libfwsi_known_folder_identifier_definition_t libfwsi_known_folder_identifier_definitions[ ] = {

"""

  _C_FILE_FOOTER = """\

\t{ libfwsi_known_folder_identifier_unknown,
\t  "Unknown" } };

/* Retrieves a string containing the name of the folder identifier
 */
const char *libfwsi_known_folder_identifier_get_name(
             const uint8_t *known_folder_identifier )
{
\tint iterator = 0;

\tif( known_folder_identifier == NULL )
\t{
\t\treturn( "Invalid known folder identifier" );
\t}
\twhile( memory_compare(
\t        ( libfwsi_known_folder_identifier_definitions[ iterator ] ).identifier,
\t        libfwsi_known_folder_identifier_unknown,
\t        16 ) != 0 )
\t{
\t\tif( memory_compare(
\t\t     ( libfwsi_known_folder_identifier_definitions[ iterator ] ).identifier,
\t\t     known_folder_identifier,
\t\t     16 ) == 0 )
\t\t{
\t\t\tbreak;
\t\t}
\t\titerator++;
\t}
\treturn(
\t ( libfwsi_known_folder_identifier_definitions[ iterator ] ).name );
}

"""

  _H_FILE_HEADER = """\
/*
 * Known folder identifier functions
 *
 * Copyright (C) 2010-2024, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#if !defined( _LIBFWSI_SHELL_FOLDER_IDENTIFIER_H )
#define _LIBFWSI_SHELL_FOLDER_IDENTIFIER_H

#include <common.h>
#include <types.h>

#include "libfwsi_extern.h"
#include "libfwsi_libcerror.h"

#if defined( __cplusplus )
extern "C" {
#endif

/* The CLSID is stored as a little endian GUID
 */
typedef struct libfwsi_known_folder_identifier_definition libfwsi_known_folder_identifier_definition_t;

struct libfwsi_known_folder_identifier_definition
{
\t/* The identifier
\t */
\tuint8_t *identifier;

\t/* The name
\t */
\tconst char *name;
};

"""

  _H_FILE_FOOTER = """\

extern uint8_t libfwsi_known_folder_identifier_unknown[ 16 ];

LIBFWSI_EXTERN \\
const char *libfwsi_known_folder_identifier_get_name(
             const uint8_t *known_folder_identifier );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBFWSI_SHELL_FOLDER_IDENTIFIER_H ) */

"""

  def __init__(self, path):
    """Initializes a libfwsi known_folder_identifier.[ch] generator.

    Args:
      path (str): path.
    """
    super(LibfwsiKnownFolderIdentifierGenerator, self).__init__()
    self._path = path

  def GenerateCFile(self, known_folders):
    """Generates the C source code file.

    Args:
      known_folders (dict[str, KnownFolderDefinition]): known folders per name.
    """
    output_path = os.path.join(
        self._path, 'libfwsi', 'libfwsi_known_folder_identifier.c')
    with open(output_path, 'w', encoding='utf8') as file_object:
      file_object.write(self._C_FILE_HEADER)

      for name, known_folder_definition in sorted(known_folders.items()):
        identifier = uuid.UUID(known_folder_definition.identifier)
        byte_values = ', '.join(
            f'0x{byte_value:02x}' for byte_value in identifier.bytes_le)

        file_object.write((
            f'uint8_t libfwsi_known_folder_identifier_{name:s}[ 16 ] = {{\n'
            f'\t{byte_values:s} }};\n'
            '\n'))

      file_object.write(self._C_FILE_MIDDLE)

      for name, known_folder_definition in sorted(known_folders.items()):
        name_string = known_folder_definition.display_name
        if 'delegate folder that appears in ' in name_string:
          name_string = name_string.replace(
              'delegate folder that appears in ', '')
          name_string = ''.join([name_string, ' (delegate folder)'])

        file_object.write((
            f'\t{{ libfwsi_known_folder_identifier_{name:s},\n'
            f'\t  "{name_string:s}" }},\n'))

      file_object.write(self._C_FILE_FOOTER)

  def GenerateHFile(self, known_folders):
    """Generates the H source code file.

    Args:
      known_folders (dict[str, KnownFolderDefinition]): known folders per name.
    """
    output_path = os.path.join(
        self._path, 'libfwsi', 'libfwsi_known_folder_identifier.h')
    with open(output_path, 'w', encoding='utf8') as file_object:
      file_object.write(self._H_FILE_HEADER)

      for name in sorted(known_folders):
        file_object.write((
            f'extern uint8_t '
            f'libfwsi_known_folder_identifier_{name:s}[ 16 ];\n'))

      file_object.write(self._H_FILE_FOOTER)


class LibfwsiShellFolderIdentifierGenerator(object):
  """Generator for libfwsi shell_folder_identifier.[ch] source code."""

  _C_FILE_HEADER = """\
/*
 * Shell folder identifier functions
 *
 * Copyright (C) 2010-2024, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <common.h>
#include <memory.h>
#include <types.h>

#include "libfwsi_libcerror.h"
#include "libfwsi_shell_folder_identifier.h"

"""

  _C_FILE_MIDDLE = """\

uint8_t libfwsi_shell_folder_identifier_empty[ 16 ] = {
\t0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

uint8_t libfwsi_shell_folder_identifier_unknown[ 16 ] = {
\t0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff };

/* The shell folder identifiers
 */
libfwsi_shell_folder_identifier_definition_t libfwsi_shell_folder_identifier_definitions[ ] = {

"""

  _C_FILE_FOOTER = """\

\t{ libfwsi_shell_folder_identifier_unknown,
\t  "Unknown" } };

/* Retrieves a string containing the name of the folder identifier
 */
const char *libfwsi_shell_folder_identifier_get_name(
             const uint8_t *shell_folder_identifier )
{
\tint iterator = 0;

\tif( shell_folder_identifier == NULL )
\t{
\t\treturn( "Invalid shell folder identifier" );
\t}
\twhile( memory_compare(
\t        ( libfwsi_shell_folder_identifier_definitions[ iterator ] ).identifier,
\t        libfwsi_shell_folder_identifier_unknown,
\t        16 ) != 0 )
\t{
\t\tif( memory_compare(
\t\t     ( libfwsi_shell_folder_identifier_definitions[ iterator ] ).identifier,
\t\t     shell_folder_identifier,
\t\t     16 ) == 0 )
\t\t{
\t\t\tbreak;
\t\t}
\t\titerator++;
\t}
\treturn(
\t ( libfwsi_shell_folder_identifier_definitions[ iterator ] ).name );
}

"""

  _H_FILE_HEADER = """\
/*
 * Shell folder identifier functions
 *
 * Copyright (C) 2010-2024, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#if !defined( _LIBFWSI_SHELL_FOLDER_IDENTIFIER_H )
#define _LIBFWSI_SHELL_FOLDER_IDENTIFIER_H

#include <common.h>
#include <types.h>

#include "libfwsi_extern.h"
#include "libfwsi_libcerror.h"

#if defined( __cplusplus )
extern "C" {
#endif

/* The CLSID is stored as a little endian GUID
 */
typedef struct libfwsi_shell_folder_identifier_definition libfwsi_shell_folder_identifier_definition_t;

struct libfwsi_shell_folder_identifier_definition
{
\t/* The identifier
\t */
\tuint8_t *identifier;

\t/* The name
\t */
\tconst char *name;
};

"""

  _H_FILE_FOOTER = """\

extern uint8_t libfwsi_shell_folder_identifier_empty[ 16 ];
extern uint8_t libfwsi_shell_folder_identifier_unknown[ 16 ];

LIBFWSI_EXTERN \\
const char *libfwsi_shell_folder_identifier_get_name(
             const uint8_t *shell_folder_identifier );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBFWSI_SHELL_FOLDER_IDENTIFIER_H ) */

"""

  def __init__(self, path):
    """Initializes a libfwsi shell_folder_identifier.[ch] generator.

    Args:
      path (str): path.
    """
    super(LibfwsiShellFolderIdentifierGenerator, self).__init__()
    self._path = path

  def GenerateCFile(self, shell_folders):
    """Generates the C source code file.

    Args:
      shell_folders (dict[str, ShellFolderDefinition]): shell folders per name.
    """
    output_path = os.path.join(
        self._path, 'libfwsi', 'libfwsi_shell_folder_identifier.c')
    with open(output_path, 'w', encoding='utf8') as file_object:
      file_object.write(self._C_FILE_HEADER)

      for name, shell_folder_definition in sorted(shell_folders.items()):
        identifier = uuid.UUID(shell_folder_definition.identifier)
        byte_values = ', '.join(
            f'0x{byte_value:02x}' for byte_value in identifier.bytes_le)

        file_object.write((
            f'uint8_t libfwsi_shell_folder_identifier_{name:s}[ 16 ] = {{\n'
            f'\t{byte_values:s} }};\n'
            '\n'))

      file_object.write(self._C_FILE_MIDDLE)

      for name, shell_folder_definition in sorted(shell_folders.items()):
        name_string = shell_folder_definition.name
        if 'delegate folder that appears in ' in name_string:
          name_string = name_string.replace(
              'delegate folder that appears in ', '')
          name_string = ''.join([name_string, ' (delegate folder)'])

        file_object.write((
            f'\t{{ libfwsi_shell_folder_identifier_{name:s},\n'
            f'\t  "{name_string:s}" }},\n'))

      file_object.write(self._C_FILE_FOOTER)

  def GenerateHFile(self, shell_folders):
    """Generates the H source code file.

    Args:
      shell_folders (dict[str, ShellFolderDefinition]): shell folders per name.
    """
    output_path = os.path.join(
        self._path, 'libfwsi', 'libfwsi_shell_folder_identifier.h')
    with open(output_path, 'w', encoding='utf8') as file_object:
      file_object.write(self._H_FILE_HEADER)

      for name in sorted(shell_folders):
        file_object.write((
            f'extern uint8_t '
            f'libfwsi_shell_folder_identifier_{name:s}[ 16 ];\n'))

      file_object.write(self._H_FILE_FOOTER)


PLASO_SHELL_FOLDERS_PY_HEADER = """\
# -*- coding: utf-8 -*-
\"\"\"Windows shell folders helper.\"\"\"


class WindowsShellFoldersHelper(object):
  \"\"\"Windows shell folders helper.\"\"\"

  _DESCRIPTION_PER_GUID = {
"""

PLASO_SHELL_FOLDERS_PY_FOOTER = """\
  }

  @classmethod
  def GetDescription(cls, shell_folder_identifier):
    \"\"\"Retrieves the description for a specific shell folder identifier.

    Args:
      shell_folder_identifier (str): shell folder identifier in the format
          "GUID".

    Returns:
      str: description represented by the shell folder identifier or None of
          not available.
    \"\"\"
    return cls._DESCRIPTION_PER_GUID.get(shell_folder_identifier.lower(), None)
"""

def Main():
  """Entry point of console script to generate source code.

  Returns:
    int: exit code that is provided to sys.exit().
  """
  argument_parser = argparse.ArgumentParser(description=(
      'Generated Windows shell related source code.'))

  argument_parser.add_argument(
      '-f', '--format', dest='format', action='store', metavar='FORMAT',
      default='plaso', help='output format.')

  argument_parser.add_argument(
      'output', nargs='?', action='store', metavar='PATH', default=None,
      help='path of the output source code.')

  options = argument_parser.parse_args()

  if not os.path.isdir(options.output):
    print(f'No such output directory: {options.output:s}.')
    print('')
    argument_parser.print_help()
    print('')
    return False

  if options.format not in ('libfwsi', 'plaso'):
    print(f'Unsupported output format: {options.format:s}')
    print('')
    argument_parser.print_help()
    print('')
    return 1

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

  if options.format == 'libfwsi':
    control_panel_items_per_name = {}
    for control_panel_item_definition in control_panel_items.values():
      name = control_panel_item_definition.module_name
      if not name or name[0] == '@':
        continue

      name = name.lower()
      name = name.replace(' ', '_')
      name = name.replace('-', '')
      name = name.replace('&', 'and')

      if name in control_panel_items_per_name:
        new_name = name
        name_suffix = 2
        while new_name in control_panel_items_per_name:
          new_name = f'{name:s}{name_suffix:d}'
          name_suffix += 1

        name = new_name

      control_panel_items_per_name[name] = control_panel_item_definition

    generator = LibfwsiControlPanelItemIdentifierGenerator(options.output)
    generator.GenerateCFile(control_panel_items_per_name)
    generator.GenerateHFile(control_panel_items_per_name)

  # TODO: add plaso output

  definitions_file = yaml_definitions_file.YAMLKnownFoldersDefinitionsFile()

  known_folders = {}

  path = os.path.join(data_path, 'defined_knownfolders.yaml')
  for known_folder_definition in definitions_file.ReadFromFile(path):
    lookup_key = known_folder_definition.identifier
    if lookup_key in known_folders:
      known_folders[lookup_key].Merge(known_folder_definition)
    else:
      known_folders[known_folder_definition.identifier] = (
          known_folder_definition)

  path = os.path.join(data_path, 'observed_knownfolders.yaml')
  for known_folder_definition in definitions_file.ReadFromFile(path):
    lookup_key = known_folder_definition.identifier
    if lookup_key in known_folders:
      known_folders[lookup_key].Merge(known_folder_definition)
    else:
      known_folders[known_folder_definition.identifier] = (
          known_folder_definition)

  if options.format == 'libfwsi':
    known_folders_per_name = {}
    for known_folder_definition in known_folders.values():
      name = known_folder_definition.display_name
      if not name or name[0] == '@':
        continue

      if name[0] == '%' and name[-1] == '%':
        name = known_folder_definition.alternate_display_names[0]
      else:
        onedrive_name = None
        for name in known_folder_definition.alternate_display_names:
          if name.startswith('OneDrive'):
            onedrive_name = name
        if onedrive_name:
          name = onedrive_name

      name = name.lower()
      name = name.replace(' ', '_')
      name = name.replace('-', '')
      name = name.replace('&', 'and')

      if 'delegate_folder_that_appears_in_' in name:
        name = name.replace('delegate_folder_that_appears_in_', '')
        name = f'{name:s}_delegate_folder'

      if name in known_folders_per_name:
        new_name = name
        name_suffix = 2
        while new_name in known_folders_per_name:
          new_name = f'{name:s}{name_suffix:d}'
          name_suffix += 1

        name = new_name

      known_folders_per_name[name] = known_folder_definition

    generator = LibfwsiKnownFolderIdentifierGenerator(options.output)
    generator.GenerateCFile(known_folders_per_name)
    generator.GenerateHFile(known_folders_per_name)

  # TODO: add plaso output

  definitions_file = yaml_definitions_file.YAMLShellFoldersDefinitionsFile()

  shell_folders = {}

  path = os.path.join(data_path, 'observed_shellfolders.yaml')
  for shell_folder_definition in definitions_file.ReadFromFile(path):
    shell_folders[shell_folder_definition.identifier] = shell_folder_definition

  if options.format == 'libfwsi':
    shell_folders_per_name = {}
    for shell_folder_definition in shell_folders.values():
      name = shell_folder_definition.name
      if not name or name[0] == '@':
        continue

      name = name.lower()
      name = name.replace(' ', '_')
      name = name.replace('-', '')
      name = name.replace('&', 'and')
      if name.endswith('...'):
        name = name[:-3]

      if 'delegate_folder_that_appears_in_' in name:
        name = name.replace('delegate_folder_that_appears_in_', '')
        name = f'{name:s}_delegate_folder'

      if name in shell_folders_per_name:
        new_name = name
        name_suffix = 2
        while new_name in shell_folders_per_name:
          new_name = f'{name:s}{name_suffix:d}'
          name_suffix += 1

        name = new_name

      shell_folders_per_name[name] = shell_folder_definition

    generator = LibfwsiShellFolderIdentifierGenerator(options.output)
    generator.GenerateCFile(shell_folders_per_name)
    generator.GenerateHFile(shell_folders_per_name)

  elif options.format == 'plaso':
    # TODO: move to generator class.
    output_path = os.path.join(
        options.output, 'plaso', 'helpers', 'windows', 'shell_folders.py')
    with open(output_path, 'w', encoding='utf8') as file_object:
      file_object.write(PLASO_SHELL_FOLDERS_PY_HEADER)

      for shell_folder_identifier, shell_folder_definition in sorted(
          shell_folders):
        name = shell_folder_definition.name
        if not name:
          name = shell_folder_definition.class_name
        if not name:
          continue

        line = f'      \'{shell_folder_identifier:s}\': \'{name:s}\',\n'
        if len(line) <= 80:
          file_object.write(line)
        else:
          file_object.write((
              f'      \'{shell_folder_identifier:s}\': (\n'
              f'          \'{name:s}\'),\n'))

  return 0


if __name__ == '__main__':
  sys.exit(Main())
