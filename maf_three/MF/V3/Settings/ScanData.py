from enum import Enum
from typing import List


class ScanData:
    # Scan data request.
    # Scan buffer type.
    class Buffer(Enum):
        Position = "Position"  # Vertex position.
        Normal = "Normal"  # Vertex normal.
        Color = "Color"  # Vertex color.
        UV = "UV"  # Vertex UVs
        Triangle = "Triangle"  # Triangle index.
        Texture = "Texture"  # Texture.
        All = "All"  # All buffer types.

    # Scan metadata type.
    class Metadata(Enum):
        Mean = "Mean"  # The mean (centroid) of the vertex positions.
        StdDev = "StdDev"  # The standard deviation of the vertex positions.
        AxisAlignedBoundingBox = "AxisAlignedBoundingBox"  # The axis-aligned bounding box of the vertex positions.

    # The merge processing step.
    class MergeStep(Enum):
        Combined = "Combined"  # The scan meshes are simply combined into a single mesh.
        Remeshed = "Remeshed"  # The combined mesh is remeshed to give a single geometric surface.
        Simplified = "Simplified"  # The combined or remeshed mesh is simplified to a reduced number of triangles.
        Textured = "Textured"  # The merged mesh has been textured.

    def __init__(self, index: int, mergeStep: 'MergeStep' = None, buffers: List['Buffer'] = None, metadata: List['Metadata'] = None):
        # Requested index of the scan in the current open project.
        self.index = index
        # The merge process step if requesting merge data.
        self.mergeStep = mergeStep
        # Requested scan buffers.
        self.buffers = buffers
        # Requested scan metadata.
        self.metadata = metadata


