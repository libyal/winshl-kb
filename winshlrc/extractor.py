# -*- coding: utf-8 -*-
"""Windows shell extractor."""

import logging

from dfimagetools import windows_registry

from dfvfs.helpers import volume_scanner as dfvfs_volume_scanner
from dfvfs.resolver import resolver as dfvfs_resolver

from dfwinreg import registry as dfwinreg_registry

from winshlrc import resource_file


class ShellFolder(object):
  """Windows shell folder.

  Attributes:
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

    # Window NT variants.
    kernel_executable_path = '\\'.join([
        system_root, 'System32', 'ntoskrnl.exe'])
    message_file = self._OpenMessageResourceFile(kernel_executable_path)

    if not message_file:
      # Window 9x variants.
      kernel_executable_path = '\\'.join([
          system_root, 'System32', '\\kernel32.dll'])
      message_file = self._OpenMessageResourceFile(kernel_executable_path)

    if not message_file:
      return None

    return message_file.file_version

  def _OpenMessageResourceFile(self, windows_path):
    """Opens the message resource file specified by the Windows path.

    Args:
      windows_path (str): Windows path containing the message resource
          filename.

    Returns:
      MessageResourceFile: message resource file or None.
    """
    path_spec = self._path_resolver.ResolvePath(windows_path)
    if path_spec is None:
      return None

    return self._OpenMessageResourceFileByPathSpec(path_spec)

  def _OpenMessageResourceFileByPathSpec(self, path_spec):
    """Opens the message resource file specified by the path specification.

    Args:
      path_spec (dfvfs.PathSpec): path specification.

    Returns:
      MessageResourceFile: message resource file or None.
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

    message_file = resource_file.MessageResourceFile(
        windows_path, ascii_codepage=self.ascii_codepage,
        preferred_language_identifier=self.preferred_language_identifier)
    message_file.OpenFileObject(file_object)

    return message_file

  def CollectShellFolders(self):
    """Retrieves shell folders

    Yields:
      ShellFolder: shell folder.
    """
    class_identifiers_key = self._registry.GetKeyByPath(
        self._CLASS_IDENTIFIERS_KEY_PATH)
    if class_identifiers_key:
      for class_identifier_key in class_identifiers_key.GetSubkeys():
        shell_folder_identifier = class_identifier_key.name[1:-1].lower()

        shell_folder_key = class_identifier_key.GetSubkeyByName('ShellFolder')
        if shell_folder_key:
          value = class_identifier_key.GetValueByName('')
          if value:
            # The value data type does not have to be a string therefore try to
            # decode the data as an UTF-16 little-endian string and strip
            # the trailing end-of-string character
            name = value.data.decode('utf-16-le').rstrip('\x00')
          else:
            name = None

          # TODO: resolve name MUI paths.

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
