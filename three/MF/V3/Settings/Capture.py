from MF.V3.Settings.Quality import Quality as MF_V3_Settings_Quality_Quality
from typing import List


class Capture:

    """
     Capture settings.
    """
    def __init__(self, quality: MF_V3_Settings_Quality_Quality = None, texture: bool = None, calibrationCard: bool = None, horizontalFrequencies: List[int] = None, verticalFrequencies: List[int] = None, blendCount: int = None, horizontalBlendFrequency: int = None, verticalBlendFrequency: int = None):
        # Capture quality preset.
        self.quality = quality
        # Capture texture.
        self.texture = texture
        # Detect the calibration card.
        self.calibrationCard = calibrationCard
        # Horizontal pattern frequencies.
        self.horizontalFrequencies = horizontalFrequencies
        # Vertical pattern frequencies.
        self.verticalFrequencies = verticalFrequencies
        # The number of capture images blended together for noise reduction.
        self.blendCount = blendCount
        # The starting horizontal frequency for blending capture images for noise reduction.
        self.horizontalBlendFrequency = horizontalBlendFrequency
        # The starting vertical frequency for blending capture images for noise reduction.
        self.verticalBlendFrequency = verticalBlendFrequency


