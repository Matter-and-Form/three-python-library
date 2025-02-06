from MF.V3.Descriptors.Project import Project as MF_V3_Descriptors_Project_Project
from enum import Enum
from typing import List


class Import:

    """
     Import scan descriptor.
    """
    class Error(Enum):

        """
         Import error codes.
        """
        Unspecified = "Unspecified"  # The error is unspecified.
        FileNotSupported = "FileNotSupported"  # The file format is not supported.
        CannotReadFile = "CannotReadFile"  # The file format is supported but cannot be read.
        MeshIsEmpty = "MeshIsEmpty"  # The imported mesh has no faces.
        NotEnoughStorage = "NotEnoughStorage"  # There is not enough filesystem memory to store the mesh.

    class Imported:

        """
         A file that was successfully imported to the project.
        """
        def __init__(self, file: str):
            # The file name.
            self.file = file

    class Ignored:

        """
         A file that failed to be imported to the project.
        """
        def __init__(self, file: str, error: 'Import.Error'):
            # The file name.
            self.file = file
            # The import error code.
            self.error = error

    def __init__(self, groups: MF_V3_Descriptors_Project_Project.Group, imported: List['Imported'] = None, ignored: List['Ignored'] = None):
        # The updated project group tree.
        self.groups = groups
        # The list of successfully imported files.
        self.imported = imported
        # The list of ignored files.
        self.ignored = ignored


