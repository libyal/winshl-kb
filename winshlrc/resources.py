# -*- coding: utf-8 -*-
"""Windows shell resources."""


class ShellFolderDefinition(object):
  """Windows shell folder definition.

  Attributes:
    alternate_names (list[str]): alternate names.
    class_name (str): class name.
    identifier (str): identifier.
    names (set[str]): names.
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
