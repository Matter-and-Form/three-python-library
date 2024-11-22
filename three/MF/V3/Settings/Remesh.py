from enum import Enum


class Remesh:
    # Field aligned remesh settings.
    # Types of remesh output.
    class Type(Enum):
        triangle = "triangle"  # Triangle mesh output.
        quad = "quad"  # Quad mesh output.
        quadDominant = "quadDominant"  # Quad-dominant mesh output.

    def __init__(self, scan: int, type: 'Type' = None, scale: float = None, faceCount: int = None, vertexCount: int = None, creaseAngleThreshold: float = None, extrinsicSmoothness: bool = None, alignToBoundaries: bool = None, smoothIterations: int = None, knnPoints: int = None, deterministic: bool = None):
        # The scan index.
        self.scan = scan
        # The type of output mesh.
        self.type = type
        # Scale
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


