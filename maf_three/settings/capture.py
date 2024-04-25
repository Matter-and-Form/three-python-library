
from enum import Enum

from array import *

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
            calibrationCard: bool|None = None, 
            texture: bool|None = None,
            quality: CaptureQuality|None = None, 
            horizontalFrequencies: array|None = None,
            verticalFrequencies: array|None = None
            ):
        
        self.calibrationCard = calibrationCard
        self.texture = texture
        self.quality = quality
        self.horizontalFrequencies = horizontalFrequencies
        self.verticalFrequencies = verticalFrequencies
