
from enum import Enum

class CaptureQuality(str, Enum):
    # Low quality.
    Low = 'Low',
    # Medium quality.
    Medium = 'Medium',
    # High quality.
    High = 'High'

class Capture:
    def __init__(
            self,
            calibrationCard = None, 
            texture = None,
            quality = None, 
            horizontalFrequencies=None,
            verticalFrequencies=None
            ):
        
        self.calibrationCard = calibrationCard
        self.texture = texture
        self.quality = quality
        self.horizontalFrequencies = horizontalFrequencies
        self.verticalFrequencies = verticalFrequencies
