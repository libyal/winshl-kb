# -*- coding: utf-8 -*-
"""Windows shell resources."""


class ControlPanelItemDefinition(object):
  """Windows control panel item definition.

  Attributes:
    alternate_module_names (list[str]): alternate module names.
    identifier (str): identifier.
    module_name (str): module name.
    name (str): name.
    windows_versions (list[str]): Windows versions.
  """

  def __init__(self):
    """Initializes a Windows control panel item definition."""
    super(ControlPanelItemDefinition, self).__init__()
    self.alternate_module_names = []
    self.identifier = None
    self.module_name = None
    self.name = None
    self.windows_versions = []


class KnownFolderDefinition(object):
  """Windows known folder definition.

  Attributes:
    alternate_display_names (list[str]): alternate display names.
    csidl (list[str]): CSIDLs that correspond to the known folder.
    default_path (str): default path.
    display_name (str): display name.
    identifier (str): identifier.
    legacy_default_path (str): legacy default path.
    legacy_display_name (str): legacy display name.
    name (str): name.
    windows_versions (list[str]): Windows versions.
  """

  def __init__(self):
    """Initializes a Windows known folder definition."""
    super(KnownFolderDefinition, self).__init__()
    self.alternate_display_names = []
    self.csidl = []
    self.default_path = None
    self.display_name = None
    self.identifier = None
    self.legacy_display_name = None
    self.legacy_default_path = None
    self.name = None
    self.windows_versions = []

  def Merge(self, other):
    """Merges the values of another known folder into the current one.

    Args:
      other (KnownFolderDefinition): known folder definition to merge values
          from.

    Raises:
      ValueError: if the known folders cannot be merged.
    """
    if self.identifier != other.identifier:
      raise ValueError('Known folder identifier mismatch.')

    if not self.default_path:
      self.default_path = other.default_path
    elif other.default_path and self.default_path != other.default_path:
      raise ValueError('Known folder default path mismatch.')

    if not self.display_name:
      self.display_name = other.display_name
    elif (other.display_name and
          other.display_name not in self.alternate_display_names):
      self.alternate_display_names.append(other.display_name)

    if not self.legacy_display_name:
      self.legacy_display_name = other.legacy_display_name
    elif (other.legacy_display_name and
          self.legacy_display_name != other.legacy_display_name):
      raise ValueError('Known folder legacy display name mismatch.')

    if not self.legacy_default_path:
      self.legacy_default_path = other.legacy_default_path
    elif (other.legacy_default_path and
          self.legacy_default_path != other.legacy_default_path):
      raise ValueError('Known folder legacy default path mismatch.')

    if not self.name:
      self.name = other.name
    elif other.name and self.name != other.name:
      raise ValueError('Known folder name mismatch.')

    alternate_display_names = set(self.alternate_display_names)
    alternate_display_names.update(other.alternate_display_names)
    self.alternate_display_names = list(alternate_display_names)

    csidl = set(self.csidl)
    csidl.update(other.csidl)
    self.csidl = list(csidl)

    windows_versions = set(self.windows_versions)
    windows_versions.update(other.windows_versions)
    self.windows_versions = list(windows_versions)


class ShellFolderDefinition(object):
  """Windows shell folder definition.

  Attributes:
    alternate_names (list[str]): alternate names.
    class_name (str): class name.
    identifier (str): identifier.
    name (str): name.
    windows_versions (list[str]): Windows versions.
  """

  def __init__(self):
    """Initializes a Windows shell folder definition."""
    super(ShellFolderDefinition, self).__init__()
    self.alternate_names = []
    self.class_name = None
    self.identifier = None
    self.name = None
    self.windows_versions = []
