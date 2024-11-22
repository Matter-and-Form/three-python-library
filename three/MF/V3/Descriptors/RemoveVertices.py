from MF.V3.Descriptors.Project import Project as MF_V3_Descriptors_Project_Project
from typing import List


class RemoveVertices:

    """
     Descriptor a remove vertices task.
    """
    class Scan:

        """
         Scan vertex and triangle removal metadata.
        """
        def __init__(self, index: int, vertices: int, triangles: int):
            # The scan index.
            self.index = index
            # The number of vertices after the removal.
            self.vertices = vertices
            # The number of triangles after the removal.
            self.triangles = triangles

    def __init__(self, scans: List['Scan'] = None, groups: MF_V3_Descriptors_Project_Project.Group = None):
        # The list of scans whose vertices were removed.
        self.scans = scans
        """
        The updated project data after undo or redo.
        If undefined, then there was no change to the project.
        """
        self.groups = groups


