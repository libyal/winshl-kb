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
    alternate_names (list[str]): alternate names.
    identifier (str): identifier.
    name (str): name.
    windows_versions (list[str]): Windows versions.
  """

  def __init__(self):
    """Initializes a Windows known folder definition."""
    super(KnownFolderDefinition, self).__init__()
    self.alternate_names = []
    self.identifier = None
    self.name = None
    self.windows_versions = []


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
