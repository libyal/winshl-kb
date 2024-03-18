# -*- coding: utf-8 -*-
"""Windows shell extractor."""

import logging

import pywrc

from dfimagetools import windows_registry

from dfvfs.helpers import volume_scanner as dfvfs_volume_scanner
from dfvfs.resolver import resolver as dfvfs_resolver

from dfwinreg import registry as dfwinreg_registry

from winshlrc import resource_file


class ShellFolder(object):
  """Windows shell folder.

  Attributes:
    alternate_names (list[str]): alternate names.
    class_name (str): class name (CLSID).
    identifier (str): identifier (GUID).
    name (str): name.
    localized_string (str): localized string of the name.
  """

  def __init__(self, identifier=None, localized_string=None):
    """Initializes a Windows Shell folder.

    Args:
      identifier (Optional[str]): identifier (GUID).
      localized_string (Optional[str]): localized string of the name.
    """
    super(ShellFolder, self).__init__()
    self.alternate_names = []
    self.class_name = None
    self.identifier = identifier
    self.localized_string = localized_string
    self.name = None


class WindowsShellExtractor(dfvfs_volume_scanner.WindowsVolumeScanner):
  """Windows shell extractor.

  Attributes:
    ascii_codepage (str): ASCII string codepage.
    preferred_language_identifier (int): preferred language identifier (LCID).
  """

  _CLASS_IDENTIFIERS_KEY_PATH = 'HKEY_LOCAL_MACHINE\\Software\\Classes\\CLSID'

  def __init__(self, debug=False, mediator=None):
    """Initializes a Windows shell extractor.

    Args:
      debug (Optional[bool]): True if debug information should be printed.
      mediator (dfvfs.VolumeScannerMediator): a volume scanner mediator or None.
    """
    super(WindowsShellExtractor, self).__init__(mediator=mediator)
    self._debug = debug
    self._format_scanner = None
    self._registry = None
    self._windows_version = None

    self.ascii_codepage = 'cp1252'
    self.preferred_language_identifier = 0x0409

  @property
  def windows_version(self):
    """The Windows version (getter)."""
    if self._windows_version is None:
      self._windows_version = self._GetWindowsVersion()
    return self._windows_version

  @windows_version.setter
  def windows_version(self, value):
    """The Windows version (setter)."""
    self._windows_version = value

  def _CollectShellFoldersFromKey(self, class_identifiers_key):
    """Retrieves shell folders from a Windows Registry key.

    Args:
      class_identifiers_key (dfwinreg.RegistryKey): class identifiers Windows
          Registry key.

    Yields:
      ShellFolder: shell folder.
    """
    for class_identifier_key in class_identifiers_key.GetSubkeys():
      shell_folder_identifier = class_identifier_key.name.lower()
      if (shell_folder_identifier[0] == '{' and
          shell_folder_identifier[-1] == '}'):
        shell_folder_identifier = shell_folder_identifier[1:-1]

      shell_folder_key = class_identifier_key.GetSubkeyByName('ShellFolder')
      if shell_folder_key:
        name = self._GetShellFolderName(class_identifier_key)

        if name and name[0] == '@' and ',-' in name:
          path, string_identifier = name[1:].rsplit(',-', maxsplit=1)
          if ';' in string_identifier:
            string_identifier, _ = string_identifier.rsplit(';', maxsplit=1)
          elif '#' in string_identifier:
            string_identifier, _ = string_identifier.rsplit('#', maxsplit=1)
          elif '@' in string_identifier:
            string_identifier, _ = string_identifier.rsplit('@', maxsplit=1)

          windows_resource_file = self._GetStringResourceFile(path)
          if windows_resource_file:
            try:
              string_identifier = int(string_identifier, 10)
              name = self._GetString(windows_resource_file, string_identifier)

            except ValueError:
              pass

        value = class_identifier_key.GetValueByName('LocalizedString')
        if value:
          # The value data type does not have to be a string therefore try to
          # decode the data as an UTF-16 little-endian string and strip
          # the trailing end-of-string character
          localized_string = value.data.decode('utf-16-le').rstrip('\x00')
        else:
          localized_string = None

        shell_folder = ShellFolder(
            identifier=shell_folder_identifier,
            localized_string=localized_string)
        if name and name.startswith('CLSID_'):
          shell_folder.class_name = name
        else:
          shell_folder.name = name

        yield shell_folder

  def _GetMUIWindowsResourceFile(self, windows_path, windows_resource_file):
    """Retrieves a MUI resource file.

    Args:
      windows_path (str): Windows path of the language neutral resource file.
      windows_resource_file (WindowsResourceFile): language neutral resource
          file.

    Returns:
      WindowsResourceFile: MUI resource file or None if not available.
    """
    mui_language = windows_resource_file.GetMUILanguage()
    if not mui_language:
      return None

    path, _, name = windows_path.rpartition('\\')

    mui_windows_path = '\\'.join([path, mui_language, f'{name:s}.mui'])
    mui_windows_resource_file = self._OpenWindowsResourceFile(
        mui_windows_path)

    if not mui_windows_resource_file:
      mui_windows_path = '\\'.join([path, f'{name:s}.mui'])
      mui_windows_resource_file = self._OpenWindowsResourceFile(
          mui_windows_path)

    if mui_windows_resource_file:
      logging.info((
          f'Resource file: {windows_path:s} references MUI resource file: '
          f'{mui_windows_path:s}'))

    return mui_windows_resource_file

  def _GetShellFolderName(self, class_identifier_key):
    """Retrieves the shell folder name.

    Args:
      class_identifier_key (dfwinreg.RegistryKey): class identifier Windows
          Registry key.

    Returns:
      str: shell folder name or None if not available.
    """
    value = class_identifier_key.GetValueByName('')
    if not value or not value.data:
      return None

    # First try to decode the value data as an UTF-16 little-endian string with
    # end-of-string character
    try:
      return value.data.decode('utf-16-le').rstrip('\x00')
    except UnicodeDecodeError:
      pass

    # Next try to decode the value data as an ASCII string with a specific
    # codepage and end-of-string character.
    try:
      return value.data.decode(self.ascii_codepage).rstrip('\x00')
    except UnicodeDecodeError:
      pass

    return None

  def _GetString(self,  windows_resource_file, string_identifier):
    """Retrieves a string from a Windows resource file.

    Args:
      windows_resource_file (WindowsResourceFile): Windows resource file.
      string_identifier (int): string identifier.

    Returns:
      str: string or None if not available.
    """
    wrc_resource = windows_resource_file.GetStringTableResource()
    if not wrc_resource:
      return None

    for wrc_resource_item in wrc_resource.items:
      base_string_identifier = wrc_resource_item.identifier * 16
      if string_identifier <= base_string_identifier + 16:
        wrc_resource_sub_item = wrc_resource_item.sub_items[0]
        resource_data = wrc_resource_sub_item.read()

        string_table_resource = pywrc.string_table_resource()
        string_table_resource.copy_from_byte_stream(
            resource_data, wrc_resource_item.identifier)

        for index in range(string_table_resource.number_of_strings):
          stored_string_identifier = (
              string_table_resource.get_string_identifier(index))
          if string_identifier == stored_string_identifier:
            return string_table_resource.get_string(index)

    return None

  def _GetStringResourceFile(self, windows_path):
    """Retrieves a string resource.

    Args:
      windows_path (str): Windows path of the Windows resource file.

    Returns:
      WindowsResourceFile: string resource file or None if not available.
    """
    windows_resource_file = None

    path_spec = self._path_resolver.ResolvePath(windows_path)
    if path_spec:
      windows_resource_file = self._OpenWindowsResourceFileByPathSpec(path_spec)

    if not windows_resource_file:
      logging.warning(f'Missing resource file: {windows_path:s}')
      return None

    if not windows_resource_file.HasStringTableResource():
      # Windows Vista and later use a MUI resource to redirect to
      # a language specific resource file.
      mui_windows_resource_file = self._GetMUIWindowsResourceFile(
          windows_path, windows_resource_file)
      if mui_windows_resource_file:
        windows_resource_file.Close()

        windows_resource_file = mui_windows_resource_file

    if not windows_resource_file.HasStringTableResource():
      logging.warning((
          f'String table resource missing from resource file: '
          f'{windows_path:s}'))

      windows_resource_file.Close()

      return None

    return windows_resource_file

  def _GetSystemRoot(self):
    """Determines the value of %SystemRoot%.

    Returns:
      str: value of SystemRoot or None if the value cannot be determined.
    """
    current_version_key = self._registry.GetKeyByPath(
        'HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows NT\\CurrentVersion')

    system_root = None
    if current_version_key:
      system_root_value = current_version_key.GetValueByName('SystemRoot')
      if system_root_value:
        system_root = system_root_value.GetDataAsObject()

    if not system_root:
      system_root = self._windows_directory

    return system_root

  def _GetWindowsVersion(self):
    """Determines the Windows version from kernel executable file.

    Returns:
      str: Windows version or None otherwise.
    """
    system_root = self._GetSystemRoot()

    # Windows NT variants.
    kernel_executable_path = '\\'.join([
        system_root, 'System32', 'ntoskrnl.exe'])
    windows_resource_file = self._OpenWindowsResourceFile(
         kernel_executable_path)

    if not windows_resource_file:
      # Windows 9x variants.
      kernel_executable_path = '\\'.join([
          system_root, 'System32', '\\kernel32.dll'])
      windows_resource_file = self._OpenWindowsResourceFile(
          kernel_executable_path)

    if not windows_resource_file:
      # Windows Me variant.
      kernel_executable_path = '\\'.join([
          system_root, 'System', '\\kernel32.dll'])
      windows_resource_file = self._OpenWindowsResourceFile(
          kernel_executable_path)

    if not windows_resource_file:
      return None

    return windows_resource_file.file_version

  def _OpenWindowsResourceFile(self, windows_path):
    """Opens the Windows resource file specified by the Windows path.

    Args:
      windows_path (str): Windows path of the Windows resource file.

    Returns:
      WindowsResourceFile: Windows resource file or None.
    """
    path_spec = self._path_resolver.ResolvePath(windows_path)
    if path_spec is None:
      return None

    return self._OpenWindowsResourceFileByPathSpec(path_spec)

  def _OpenWindowsResourceFileByPathSpec(self, path_spec):
    """Opens the Windows resource file specified by the path specification.

    Args:
      path_spec (dfvfs.PathSpec): path specification.

    Returns:
      WindowsResourceFile: Windows resource file or None.
    """
    windows_path = self._path_resolver.GetWindowsPath(path_spec)
    if windows_path is None:
      logging.warning('Unable to retrieve Windows path.')

    try:
      file_object = dfvfs_resolver.Resolver.OpenFileObject(path_spec)
    except IOError as exception:
      logging.warning(
          f'Unable to open: {path_spec.comparable:s} with error: {exception!s}')
      file_object = None

    if file_object is None:
      return None

    windows_resource_file = resource_file.WindowsResourceFile(
        windows_path, ascii_codepage=self.ascii_codepage,
        preferred_language_identifier=self.preferred_language_identifier)
    windows_resource_file.OpenFileObject(file_object)

    return windows_resource_file

  def CollectShellFolders(self):
    """Retrieves shell folders

    Yields:
      ShellFolder: shell folder.
    """
    class_identifiers_key = self._registry.GetKeyByPath(
        self._CLASS_IDENTIFIERS_KEY_PATH)
    if class_identifiers_key:
      yield from self._CollectShellFoldersFromKey(class_identifiers_key)

    # TODO: Add support for per-user shell folders

  def ScanForWindowsVolume(self, source_path, options=None):
    """Scans for a Windows volume.

    Args:
      source_path (str): source path.
      options (Optional[VolumeScannerOptions]): volume scanner options. If None
          the default volume scanner options are used, which are defined in the
          VolumeScannerOptions class.

    Returns:
      bool: True if a Windows volume was found.

    Raises:
      ScannerError: if the source path does not exists, or if the source path
          is not a file or directory, or if the format of or within
          the source file is not supported.
    """
    result = super(WindowsShellExtractor, self).ScanForWindowsVolume(
        source_path, options=options)
    if not result:
      return False

    registry_file_reader = (
        windows_registry.StorageMediaImageWindowsRegistryFileReader(
            self._file_system, self._path_resolver))
    self._registry = dfwinreg_registry.WinRegistry(
        registry_file_reader=registry_file_reader)

    return True
