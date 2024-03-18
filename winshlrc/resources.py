# -*- coding: utf-8 -*-
"""Windows shell resources."""


class ControlPanelItemDefinition(object):
  """Windows control panel item definition.

  Attributes:
    identifier (str): identifier.
    module_name (str): module name.
    name (str): name.
    windows_versions (list[str]): Windows versions.
  """

  def __init__(self):
    """Initializes a Windows control panel item definition."""
    super(ControlPanelItemDefinition, self).__init__()
    self.identifier = None
    self.module_name = None
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
