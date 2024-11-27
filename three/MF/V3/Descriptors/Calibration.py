from enum import Enum
from typing import List


class Quality(Enum):

    """
     Calibration quality.
    """
    Empty = "None"  # The calibration does not exist.
    Poor = "Poor"  # Poor calibration quality.
    Fair = "Fair"  # Fair calibration quality.
    Good = "Good"  # Good calibration quality.
    Excellent = "Excellent"  # Excellent calibration quality.


class Camera:

    """
     Camera calibration descriptor.
    """
    def __init__(self, quality: 'Quality', date: List[int] = None):
        # Calibration quality.
        self.quality = quality
        # Calibration date and time [year, month, day, hour, minute, second].
        self.date = date


class Turntable:

    """
     Turntable calibration descriptor.
    """
    def __init__(self, quality: 'Quality', date: List[int] = None, focus: List[int] = None):
        # Calibration quality.
        self.quality = quality
        # Calibration date and time [year, month, day, hour, minute, second].
        self.date = date
        # Focus values of each camera during calibration.
        self.focus = focus


class CaptureTarget:
    """
    Calibration capture target.

    The camera calibration capture targets are used to draw quad overlays on the video stream to guide a user as to where to position the calibration card for each capture during camera calibration.
    """
    def __init__(self, camera: int, quads: List[float] = None):
        # Index of the camera that is displayed to the user for this capture.
        self.camera = camera
        """
        The target quad for each camera.
        This is a set of 16 numbers defining the quad coordinates on the left and right camera.
        The first 4 pairs of numbers define the quad on the left camera.
        The last 4 pairs of numbers define the quad on the right camera.
        """
        self.quads = quads


class DetectedCard:

    """
     Detected calibration card descriptor.
    """
    class Target:

        """
         Calibration capture target properties.
        """
        def __init__(self, match: float, hold: float):
            """
            A normalized value indicating how closely the calibration card matches the target
            overlay. 0 indicates a poor match.  1 indicates a good match.
            """
            self.match = match
            """
            A normalized value indicating how long the user has held the calibration card steady over
            the target overlay. When the value reaches 1, the user has held the calibration card
            steady for the complete required duration.
            """
            self.hold = hold

    def __init__(self, size: List[int] = None, quad: List[float] = None, corners: List[float] = None, target: 'Target' = None):
        # The calibration card columns and rows.
        self.size = size
        # The calibration card bounding quadrilateral.
        self.quad = quad
        # The detected corners of the calibration card.
        self.corners = corners
        # The capture target properties, if a capture target is specified.
        self.target = target


