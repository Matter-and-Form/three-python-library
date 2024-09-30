from MF.V3.Settings.Quality import Quality as MF_V3_Settings_Quality_Quality
from MF.V3.Settings.ScanSelection import ScanSelection as MF_V3_Settings_ScanSelection_ScanSelection
from enum import Enum


class Merge:
    # Scan merge settings.
    class Remesh:
        # Remesh settings.
        # Remesh method.
        class Method(Enum):
            FlowTriangles = "FlowTriangles"  # Flow remesh as triangles.
            FlowQuads = "FlowQuads"  # Flow remesh as quads.
            FlowQuadDominant = "FlowQuadDominant"  # Flow remesh as quad-dominant mesh.
            PoissonTriangles = "PoissonTriangles"  # Poisson remesh as triangles.

        class Flow:
            # Flow remesh settings
            def __init__(self, scale: float = None, faceCount: int = None, vertexCount: int = None, creaseAngleThreshold: float = None, extrinsicSmoothness: bool = None, alignToBoundaries: bool = None, smoothIterations: int = None, knnPoints: int = None, deterministic: bool = None):
                # Output resolution scale.  Smaller means more faces.
                self.scale = scale
                # The approximate number of remeshed faces.
                self.faceCount = faceCount
                # The approximate number of remeshed vertices.
                self.vertexCount = vertexCount
                # The crease angle threshold.
                self.creaseAngleThreshold = creaseAngleThreshold
                # Use extrinsic smoothness.
                self.extrinsicSmoothness = extrinsicSmoothness
                # Align mesh to boundaries.
                self.alignToBoundaries = alignToBoundaries
                # The number of smoothing iterations.
                self.smoothIterations = smoothIterations
                # The number of KNN points (point cloud input only).
                self.knnPoints = knnPoints
                # Use deterministic (repeatable) remeshing.
                self.deterministic = deterministic

        class Poisson:
            def __init__(self, voxelSize: float = None, depth: int = None, scale: float = None, linearInterpolation: bool = None):
                # Voxel size.
                self.voxelSize = voxelSize
                # Depth.
                self.depth = depth
                # Scale.
                self.scale = scale
                # Linear Interpolation.
                self.linearInterpolation = linearInterpolation

        def __init__(self, method: 'Method' = None, quality: MF_V3_Settings_Quality_Quality = None, flow: 'Flow' = None, poisson: 'Poisson' = None, voxelSize: float = None, depth: int = None, scale: float = None, linearInterpolation: bool = None):
            # Remesh method.
            self.method = method
            # Remesh quality.
            self.quality = quality
            # Flow remesh options (Ignored if method is 'Poison').
            self.flow = flow
            # Poisson remesh options (Ignored if method is not 'Poisson').
            self.poisson = poisson
            """ Temporary for backwards compatibility
             Voxel size."""
            self.voxelSize = voxelSize
            # Depth.
            self.depth = depth
            # Scale.
            self.scale = scale
            # Linear Interpolation.
            self.linearInterpolation = linearInterpolation

    class Simplify:
        # Simplify settings.
        def __init__(self, triangleCount: int):
            # Target triangle count.
            self.triangleCount = triangleCount

    def __init__(self, selection: MF_V3_Settings_ScanSelection_ScanSelection = None, remesh: 'Remesh' = None, simplify: 'Simplify' = None, texturize: bool = None):
        # The scan selection.
        self.selection = selection
        # Remesh settings.
        self.remesh = remesh
        # Simplify settings.
        self.simplify = simplify
        # Apply textures to the merged mesh.
        self.texturize = texturize


