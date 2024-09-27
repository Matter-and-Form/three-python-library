from MF.V3.Settings.Quality import Quality as MF_V3_Settings_Quality_Quality
from typing import List


class Capture:
    # Capture settings.
    def __init__(self, horizontalFrequencies: List[int], verticalFrequencies: List[int], quality: MF_V3_Settings_Quality_Quality = None, texture: bool = None, calibrationCard: bool = None, blendCount: int = None, horizontalBlendFrequency: int = None, verticalBlendFrequency: int = None):
        # Horizontal pattern frequencies.
        self.horizontalFrequencies = horizontalFrequencies
        # Vertical pattern frequencies.
        self.verticalFrequencies = verticalFrequencies
        # Capture quality preset.
        self.quality = quality
        # Capture texture.
        self.texture = texture
        # Detect the calibration card.
        self.calibrationCard = calibrationCard
        # The number of capture images blended together for noise reduction.
        self.blendCount = blendCount
        # The starting horizontal frequency for blending capture images for noise reduction.
        self.horizontalBlendFrequency = horizontalBlendFrequency
        # The starting vertical frequency for blending capture images for noise reduction.
        self.verticalBlendFrequency = verticalBlendFrequency


