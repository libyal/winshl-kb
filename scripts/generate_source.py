#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to generate Windows shell related source code."""

import argparse
import logging
import os
import sys
import uuid

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
      'source', nargs='?', action='store', metavar='PATH', default=None,
      help='path of the Windows shell related data file.')

  argument_parser.add_argument(
      'output', nargs='?', action='store', metavar='PATH', default=None,
      help='path containign of the output source.')

  options = argument_parser.parse_args()

  if not options.source:
    print('Source value is missing.')
    print('')
    argument_parser.print_help()
    print('')
    return False

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

  try:
    with open(options.source, 'r', encoding='utf-8') as file_object:
      data_header = file_object.readline()

  except (SyntaxError, UnicodeDecodeError) as exception:
    print(f'Unable to read data haeader with error: {exception!s}')
    return 0

  if data_header.startswith('# winshl-kb controlpanel item definitions'):
    definitions_file = (
        yaml_definitions_file.YAMLControlPanelItemsDefinitionsFile())

    if options.format == 'libfwsi':
      control_panel_items_per_name = {}
      for control_panel_item_definition in definitions_file.ReadFromFile(
          options.source):
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

  elif data_header.startswith('# winshl-kb shellfolder definitions'):
    definitions_file = yaml_definitions_file.YAMLShellFoldersDefinitionsFile()

    if options.format == 'libfwsi':
      shell_folders_per_name = {}
      for shell_folder_definition in definitions_file.ReadFromFile(
          options.source):
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

        for shell_folder_definition in sorted(
            definitions_file.ReadFromFile(options.source),
            key=lambda definition: definition.identifier):
          name = shell_folder_definition.name
          if not name:
            name = shell_folder_definition.class_name
          if not name:
            continue

          shell_folder_identifier = shell_folder_definition.identifier

          line = f'      \'{shell_folder_identifier:s}\': \'{name:s}\',\n'
          if len(line) <= 80:
            file_object.write(line)
          else:
            file_object.write((
                f'      \'{shell_folder_identifier:s}\': (\n'
                f'          \'{name:s}\'),\n'))

  else:
    print('Unsupported data file.')
    print('')
    return 1

  return 0


if __name__ == '__main__':
  sys.exit(Main())
