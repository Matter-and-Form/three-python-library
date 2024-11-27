from enum import Enum
from typing import List


class Align:

    """
     Alignment settings.
    """
    class Points:

        """
         Point pair alignment settings.
        """
        def __init__(self, points: List[float] = None, absoluteError: float = None, relativeError: float = None, useAllPoints: bool = None):
            # The set of corresponding point pairs.
            self.points = points
            # The maximum absolute error for a point pair to be an inlier to the model.
            self.absoluteError = absoluteError
            # The maximum error relative to the size of the aligned scans for a point pair to be an inlier to the model.
            self.relativeError = relativeError
            # Ignore alignment errors and use all selected points for alignment.
            self.useAllPoints = useAllPoints

    class Ransac:

        """
         Ransac alignment settings.
        """
        def __init__(self, downsampleVoxelSize: float = None, maximumFeatureRadius: float = None, maximumFeaturePointCount: int = None, maximumMatchDistance: float = None, minimumMatchSimilarity: float = None, mutualFilter: bool = None):
            self.downsampleVoxelSize = downsampleVoxelSize
            self.maximumFeatureRadius = maximumFeatureRadius
            self.maximumFeaturePointCount = maximumFeaturePointCount
            self.maximumMatchDistance = maximumMatchDistance
            self.minimumMatchSimilarity = minimumMatchSimilarity
            self.mutualFilter = mutualFilter

    class ICP:

        """
         Iterative closest point alignment settings.
        """
        def __init__(self, matchDistance: float):
            # The maximum distance for two points to be considered a match.
            self.matchDistance = matchDistance

    class Rough:

        """
         Rough alignment settings.
        """
        class Method(Enum):

            """
             Rough alignment methods.
            """
            Empty = "None"  # No rough alignment.
            FastGlobal = "FastGlobal"  # Fast global alignment.
            Ransac = "Ransac"  # Ransac alignment.
            Points = "Points"  # Point pair alignment.

        def __init__(self, method: 'Method', ransac: 'Align.Ransac' = None, points: 'Align.Points' = None):
            # Rough alignment method.
            self.method = method
            # FastGlobal fastGlobal;
            self.ransac = ransac
            # Point pair alignment settings.
            self.points = points

    class Fine:

        """
         Fine alignment settings.
        """
        class Method(Enum):

            """
             Fine alignment methods.
            """
            Empty = "None"  # No fine alignment.
            ICP = "ICP"  # Iterative closest point alignment.

        class Transform:
            def __init__(self, rotation: List[float] = None, translation: List[float] = None):
                self.rotation = rotation
                self.translation = translation

        def __init__(self, method: 'Method', icp: 'Align.ICP' = None, initialTransform: 'Transform' = None):
            # Fine alignment method.
            self.method = method
            # Iterative closest point settings.
            self.icp = icp
            # The initial transform for fine alignment.
            self.initialTransform = initialTransform

    def __init__(self, source: int, target: int, rough: 'Rough' = None, fine: 'Fine' = None):
        # Index of the scan or group to align.
        self.source = source
        # Index of the scan or group to align to.
        self.target = target
        # Rough alignment settings.
        self.rough = rough
        # Fine alignment settings.
        self.fine = fine


