from MF.V3.Settings.Merge import Merge as MF_V3_Settings_Merge_Merge
from MF.V3.Settings.Scan import Scan as MF_V3_Settings_Scan_Scan
from typing import List


class Advanced:

    """
     Advanced settings.
    """
    class Capture:

        """
         Capture settings.
        """
        def __init__(self, horizontalFrequencies: List[int] = None, verticalFrequencies: List[int] = None, use: bool = None):
            # Projector sample rate.
            self.horizontalFrequencies = horizontalFrequencies
            # Image sample rate.
            self.verticalFrequencies = verticalFrequencies
            # Use the capture settings.
            self.use = use

    class Sampling:

        """
         Sampling settings.
        """
        def __init__(self, projectorSampleRate: float = None, imageSampleRate: float = None, use: bool = None):
            # Projector sample rate.
            self.projectorSampleRate = projectorSampleRate
            # Image sample rate.
            self.imageSampleRate = imageSampleRate
            # Use the sampling settings.
            self.use = use

    class EdgeDetection:

        """
         Edge detection settings.
        """
        def __init__(self, threshold: float = None, laplacianKernelRadius: int = None, gaussianBlurRadius: int = None, gaussianBlurStdDev: float = None, maximumWidthForProcessing: int = None, use: bool = None):
            # The edge detection threshold.
            self.threshold = threshold
            # The Laplacian kernel radius.  This must be in the range [1..5].
            self.laplacianKernelRadius = laplacianKernelRadius
            """
            Gaussian blur kernel radius. (Optional)  To disable, set to 0.

            The phase images can optionally blurred before taking the Laplacian to reduce noise.
            However as a result, the detected edges are wider.
            """
            self.gaussianBlurRadius = gaussianBlurRadius
            """
            Gaussian blur kernel standard deviation.  This parameter is ignored if
            gaussianBlurSize is zero.
            """
            self.gaussianBlurStdDev = gaussianBlurStdDev
            """
            The maximum image width for processing. (Optional) To disable, set to 0.

            If this value is greater than zero, the phase images are resized to the maximum
            width prior to computing the Laplacian and the the detected edges are then upsampled to the
            original size.

            This would be done to speed up processing or to detect edges on a larger scale.
            """
            self.maximumWidthForProcessing = maximumWidthForProcessing
            # Use the edge detection settings.
            self.use = use

    class PhaseFilter:

        """
         Phase filter settings.
        """
        def __init__(self, kernelRadius: int = None, spatialWeightStdDev: float = None, use: bool = None):
            """
            The filter kernel radius.

            A neighboring value must be within this radius to be included in the filter.
            If the kernel radius is set to zero, the phase filtering is disabled.
            """
            self.kernelRadius = kernelRadius
            """
            The standard deviation of the spatial weights.

            The weight of a neighboring value is \f$ exp(-(r/s)^2) \f$  where \f$ r \f$
            is the distance to the central value and \f$ s \f$ is the spatial weight
            standard deviation.

            If the spatial weight standard deviation is set to zero, all the spatial
            weights are uniformly set to 1.
            """
            self.spatialWeightStdDev = spatialWeightStdDev
            # Use the phase filter settings.
            self.use = use

    class AdaptiveSampling:
        """
        Adaptive sampling settings

        Adaptive sampling will downsample points in regions of low detail
        and keep points in regions of high detail.
        """
        def __init__(self, rate: float, type: MF_V3_Settings_Scan_Scan.Processing.AdaptiveSampling.Type = None, use: bool = None):
            # The sample rate [0..1] for the regions of low detail.
            self.rate = rate
            # Sampling type.
            self.type = type
            # Use the adaptive sampling settings.
            self.use = use

    class PointClipping:

        """
         Point32 clipping settings.
        """
        def __init__(self, type: MF_V3_Settings_Scan_Scan.Processing.PointClipping.Type = None, transform: List[float] = None, use: bool = None):
            # Point32 clipping type.
            self.type = type
            # 4x4 transform mapping 3D points to the canonical point32 clipping coordinates.
            self.transform = transform
            # Use the point32 clipping settings.
            self.use = use

    class NormalEstimation:

        """
         Normal estimation settings.
        """
        def __init__(self, method: MF_V3_Settings_Scan_Scan.Processing.NormalEstimation.Method = None, maximumNeighbourCount: int = None, maximumNeighbourRadius: float = None, useMaximumNeighbourCount: bool = None, useMaximumNeighbourRadius: bool = None, use: bool = None):
            # Normal estimation method.
            self.method = method
            """
            Maximum number of nearest neighbors used to compute the normal.
            This value is only used with the NORMAL_OPEN3D method.
            """
            self.maximumNeighbourCount = maximumNeighbourCount
            # Maximum radius for a point32 to be considered a neighbour.
            self.maximumNeighbourRadius = maximumNeighbourRadius
            self.useMaximumNeighbourCount = useMaximumNeighbourCount
            self.useMaximumNeighbourRadius = useMaximumNeighbourRadius
            # Use the normal estimation settings.
            self.use = use

    class OutlierRemoval:

        """
         Radius outlier removal settings.
        """
        def __init__(self, neighbourCount: int = None, neighbourRadius: float = None, use: bool = None):
            # The minimum number of points within the radius for a point32 to be retained.
            self.neighbourCount = neighbourCount
            # The neighbour search radius.
            self.neighbourRadius = neighbourRadius
            # Use the outlier removal settings.
            self.use = use

    class Remesh:

        """
         Remesh settings.
        """
        def __init__(self, quality: MF_V3_Settings_Merge_Merge.Quality = None, voxelSize: float = None, depth: int = None, scale: float = None, linearInterpolation: bool = None, use: bool = None):
            # Remesh quality preset.
            self.quality = quality
            # Voxel size.
            self.voxelSize = voxelSize
            # Depth.
            self.depth = depth
            # Scale.
            self.scale = scale
            # Linear Interpolation.
            self.linearInterpolation = linearInterpolation
            # Use the remesh settings.
            self.use = use

    class Camera:

        """
         Camera settings.
        """
        def __init__(self, useContinuousExposureValues: bool = None):
            self.useContinuousExposureValues = useContinuousExposureValues

    class Turntable:

        """
         Turntable settings.
        """
        def __init__(self, rampAngle: int = None, pointClippingRadius: float = None, pointClippingMinHeight: float = None, pointClippingMaxHeight: float = None, use: bool = None):
            # The angle in degrees to slow down the turntable at the end of a rotation.
            self.rampAngle = rampAngle
            # The radius of the point clipping cylinder.
            self.pointClippingRadius = pointClippingRadius
            # The minimum height of the point clipping cylinder.
            self.pointClippingMinHeight = pointClippingMinHeight
            # The maximum height of the point clipping cylinder.
            self.pointClippingMaxHeight = pointClippingMaxHeight
            # Use the turntable settings.
            self.use = use

    def __init__(self, capture: 'Capture' = None, sampling: 'Sampling' = None, edgeDetection: 'EdgeDetection' = None, phaseFilter: 'PhaseFilter' = None, adaptiveSampling: 'AdaptiveSampling' = None, normalEstimation: 'NormalEstimation' = None, outlierRemoval: 'OutlierRemoval' = None, remesh: 'Remesh' = None, camera: 'Camera' = None, turntable: 'Turntable' = None):
        # Capture settings.
        self.capture = capture
        # Sampling settings.
        self.sampling = sampling
        # Edge detection settings.
        self.edgeDetection = edgeDetection
        # Phase filter settings.
        self.phaseFilter = phaseFilter
        # Adaptive sampling settings.
        self.adaptiveSampling = adaptiveSampling
        # Normal estimation settings.
        self.normalEstimation = normalEstimation
        # Radius outlier removal settings.
        self.outlierRemoval = outlierRemoval
        # Remesh settings.
        self.remesh = remesh
        # Camera settings.
        self.camera = camera
        # Turntable settings.
        self.turntable = turntable


