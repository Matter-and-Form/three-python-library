from MF.V3.Settings.ScanSelection import ScanSelection as MF_V3_Settings_ScanSelection_ScanSelection
from enum import Enum


class Merge:

    """
     Scan merge settings.
    """
    class Quality(Enum):

        """
         Remesh quality settings.
        """
        VeryLow = "VeryLow"  # Very low remesh quality.
        Low = "Low"  # Low remesh quality.
        Medium = "Medium"  # Medium remesh quality.
        High = "High"  # High remesh quality.
        VeryHigh = "VeryHigh"  # Very high remesh quality.

    class Remesh:

        """
         Remesh settings.
        """
        def __init__(self, quality: 'Merge.Quality' = None, voxelSize: float = None, depth: int = None, scale: float = None, linearInterpolation: bool = None):
            # Remesh quality.
            self.quality = quality
            # Voxel size.
            self.voxelSize = voxelSize
            # Depth.
            self.depth = depth
            # Scale.
            self.scale = scale
            # Linear Interpolation.
            self.linearInterpolation = linearInterpolation

    class Simplify:

        """
         Simplify settings.
        """
        class Method(Enum):

            """
             Remesh method.
            """
            QuadraticDecimation = "QuadraticDecimation"  # Quadratic decimation.
            FlowTriangles = "FlowTriangles"  # Flow remesh as triangles.
            FlowQuads = "FlowQuads"  # Flow remesh as quads.
            FlowQuadDominant = "FlowQuadDominant"  # Flow remesh as quad-dominant mesh.

        def __init__(self, method: 'Method' = None, faceCount: int = None):
            # Simplify method.
            self.method = method
            # Target face count.
            self.faceCount = faceCount

    def __init__(self, selection: MF_V3_Settings_ScanSelection_ScanSelection = None, remesh: 'Remesh' = None, simplify: 'Simplify' = None, texturize: bool = None):
        # The scan selection.
        self.selection = selection
        # Remesh settings.
        self.remesh = remesh
        # Simplify settings.
        self.simplify = simplify
        # Apply textures to the merged mesh.
        self.texturize = texturize


