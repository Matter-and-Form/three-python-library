from MF.V3.Descriptors.Project import Project as MF_V3_Descriptors_Project_Project
from typing import List


class ProjectAction:

    """
     Descriptor for a project undo/redo action.
    """
    class Scan:

        """
         Scan vertices removal/insertion metadata.
        """
        def __init__(self, index: int, vertices: int, triangles: int):
            # The scan index.
            self.index = index
            # The number of vertices after undo or redo.
            self.vertices = vertices
            # The number of triangles after undo or redo.
            self.triangles = triangles

    def __init__(self, task: str, project: MF_V3_Descriptors_Project_Project = None, scans: List['Scan'] = None):
        # The original websocket task that the action is undoing or redoing.
        self.task = task
        """
        The updated project data after undo or redo.
        If undefined, then there was no change to the project.
        """
        self.project = project
        # The list of scans whose vertex/triangle elements were changed by the undo/redo action.
        self.scans = scans


class ProjectActions:

    """
     Project undo and redo action descriptors.
    """
    def __init__(self, undo: List[str] = None, redo: List[str] = None):
        # Project undo action descriptors.
        self.undo = undo
        # Project redo action descriptors.
        self.redo = redo


