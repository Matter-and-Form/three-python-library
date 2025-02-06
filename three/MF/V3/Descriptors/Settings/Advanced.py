from MF.V3.Settings.Scan import Scan as MF_V3_Settings_Scan_Scan
from typing import List


class Advanced:

    """
     Advanced settings descriptor.
    """
    class Use:

        """
         Use advanced settings.
        """
        def __init__(self, value: bool, default: bool):
            self.value = value
            self.default = default

    class Capture:

        """
         Capture settings descriptor.
        """
        class HorizontalFrequencies:
            def __init__(self, min: int, max: int, value: List[int] = None, default: List[int] = None):
                self.min = min
                self.max = max
                self.value = value
                self.default = default

        class VerticalFrequencies:
            def __init__(self, min: int, max: int, value: List[int] = None, default: List[int] = None):
                self.min = min
                self.max = max
                self.value = value
                self.default = default

        def __init__(self, use: 'Advanced.Use', horizontalFrequencies: 'HorizontalFrequencies', verticalFrequencies: 'VerticalFrequencies'):
            self.use = use
            self.horizontalFrequencies = horizontalFrequencies
            self.verticalFrequencies = verticalFrequencies

    class Sampling:

        """
         Sampling settings descriptor.
        """
        class ProjectorSampleRate:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class ImageSampleRate:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        def __init__(self, use: 'Advanced.Use', projectorSampleRate: 'ProjectorSampleRate', imageSampleRate: 'ImageSampleRate'):
            # Use sampling settings.
            self.use = use
            self.projectorSampleRate = projectorSampleRate
            self.imageSampleRate = imageSampleRate

    class EdgeDetection:

        """
         Edge detection settings descriptor.
        """
        class Threshold:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class LaplacianKernelRadius:
            def __init__(self, value: int, default: int, min: int, max: int):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class GaussianBlurRadius:
            def __init__(self, value: int, default: int, min: int, max: int):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class GaussianBlurStdDev:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class MaximumWidthForProcessing:
            def __init__(self, value: int, default: int, min: int, max: int):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        def __init__(self, use: 'Advanced.Use', threshold: 'Threshold', laplacianKernelRadius: 'LaplacianKernelRadius', gaussianBlurRadius: 'GaussianBlurRadius', gaussianBlurStdDev: 'GaussianBlurStdDev', maximumWidthForProcessing: 'MaximumWidthForProcessing'):
            self.use = use
            self.threshold = threshold
            self.laplacianKernelRadius = laplacianKernelRadius
            self.gaussianBlurRadius = gaussianBlurRadius
            self.gaussianBlurStdDev = gaussianBlurStdDev
            self.maximumWidthForProcessing = maximumWidthForProcessing

    class PhaseFilter:

        """
         Phase filter settings descriptor.
        """
        class KernelRadius:
            def __init__(self, value: int, default: int, min: int, max: int):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class SpatialWeightStdDev:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        def __init__(self, use: 'Advanced.Use', kernelRadius: 'KernelRadius', spatialWeightStdDev: 'SpatialWeightStdDev'):
            self.use = use
            self.kernelRadius = kernelRadius
            self.spatialWeightStdDev = spatialWeightStdDev

    class AdaptiveSampling:

        """
         Adaptive sampling settings descriptor.
        """
        class Type:
            def __init__(self, value: MF_V3_Settings_Scan_Scan.Processing.AdaptiveSampling.Type, default: MF_V3_Settings_Scan_Scan.Processing.AdaptiveSampling.Type):
                self.value = value
                self.default = default

        class Rate:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        def __init__(self, use: 'Advanced.Use', type: 'Type', rate: 'Rate'):
            self.use = use
            self.type = type
            self.rate = rate

    class NormalEstimation:

        """
         Normal estimation settings descriptor.
        """
        class Method:
            def __init__(self, value: MF_V3_Settings_Scan_Scan.Processing.NormalEstimation.Method, default: MF_V3_Settings_Scan_Scan.Processing.NormalEstimation.Method):
                self.value = value
                self.default = default

        class MaximumNeighbourCount:
            def __init__(self, value: int, default: int, min: int, max: int):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class MaximumNeighbourRadius:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class UseMaximumNeighbourCount:
            def __init__(self, value: bool, default: bool):
                self.value = value
                self.default = default

        class UseMaximumNeighbourRadius:
            def __init__(self, value: bool, default: bool):
                self.value = value
                self.default = default

        def __init__(self, use: 'Advanced.Use', method: 'Method', maximumNeighbourCount: 'MaximumNeighbourCount', maximumNeighbourRadius: 'MaximumNeighbourRadius', useMaximumNeighbourCount: 'UseMaximumNeighbourCount', useMaximumNeighbourRadius: 'UseMaximumNeighbourRadius'):
            self.use = use
            self.method = method
            self.maximumNeighbourCount = maximumNeighbourCount
            self.maximumNeighbourRadius = maximumNeighbourRadius
            self.useMaximumNeighbourCount = useMaximumNeighbourCount
            self.useMaximumNeighbourRadius = useMaximumNeighbourRadius

    class OutlierRemoval:

        """
         Outlier removal settings descriptor.
        """
        class NeighbourCount:
            def __init__(self, value: int, default: int, min: int, max: int):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class NeighbourRadius:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        def __init__(self, use: 'Advanced.Use', neighbourCount: 'NeighbourCount', neighbourRadius: 'NeighbourRadius'):
            self.use = use
            self.neighbourCount = neighbourCount
            self.neighbourRadius = neighbourRadius

    class Remesh:

        """
         Remesh settings descriptor.
        """
        class VoxelSize:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class Depth:
            def __init__(self, value: int, default: int, min: int, max: int):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class Scale:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class LinearInterpolation:
            def __init__(self, value: bool, default: bool):
                self.value = value
                self.default = default

        def __init__(self, use: 'Advanced.Use', voxelSize: 'VoxelSize', depth: 'Depth', scale: 'Scale', linearInterpolation: 'LinearInterpolation'):
            self.use = use
            self.voxelSize = voxelSize
            self.depth = depth
            self.scale = scale
            self.linearInterpolation = linearInterpolation

    class Camera:

        """
         Camera settings descriptor.
        """
        class UseContinuousExposureValues:

            """
             Use continuous exposure values settings descriptor.
            """
            def __init__(self, value: bool, default: bool):
                self.value = value
                self.default = default

        def __init__(self, useContinuousExposureValues: 'UseContinuousExposureValues'):
            # Use continuous exposure values settings descriptor.
            self.useContinuousExposureValues = useContinuousExposureValues

    class Turntable:

        """
         Turntable settings descriptor.
        """
        class RampAngle:

            """
             The angle in degrees to slow down the turntable at the end of a rotation.
            """
            def __init__(self, value: int, default: int, min: int, max: int):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class PointClippingRadius:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class PointClippingMinHeight:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        class PointClippingMaxHeight:
            def __init__(self, value: float, default: float, min: float, max: float):
                self.value = value
                self.default = default
                self.min = min
                self.max = max

        def __init__(self, use: 'Advanced.Use', rampAngle: 'RampAngle', pointClippingRadius: 'PointClippingRadius', pointClippingMinHeight: 'PointClippingMinHeight', pointClippingMaxHeight: 'PointClippingMaxHeight'):
            # Use the advanced turntable settings.
            self.use = use
            # The angle in degrees to slow down the turntable at the end of a rotation.
            self.rampAngle = rampAngle
            # The radius of the point clipping cylinder.
            self.pointClippingRadius = pointClippingRadius
            # The minimum height of the point clipping cylinder.
            self.pointClippingMinHeight = pointClippingMinHeight
            # The maximum height of the point clipping cylinder.
            self.pointClippingMaxHeight = pointClippingMaxHeight

    def __init__(self, capture: 'Capture', sampling: 'Sampling', edgeDetection: 'EdgeDetection', phaseFilter: 'PhaseFilter', adaptiveSampling: 'AdaptiveSampling', normalEstimation: 'NormalEstimation', outlierRemoval: 'OutlierRemoval', remesh: 'Remesh', camera: 'Camera', turntable: 'Turntable'):
        # Capture settings descriptor.
        self.capture = capture
        # Sampling settings descriptor.
        self.sampling = sampling
        # Edge detection settings descriptor.
        self.edgeDetection = edgeDetection
        # Phase filter settings descriptor.
        self.phaseFilter = phaseFilter
        # Adaptive sampling settings descriptor.
        self.adaptiveSampling = adaptiveSampling
        # Normal estimation settings descriptor.
        self.normalEstimation = normalEstimation
        # Outlier removal settings descriptor.
        self.outlierRemoval = outlierRemoval
        # Remesh settings descriptor.
        self.remesh = remesh
        # Camera settings descriptor.
        self.camera = camera
        # Turntable settings descriptor.
        self.turntable = turntable


