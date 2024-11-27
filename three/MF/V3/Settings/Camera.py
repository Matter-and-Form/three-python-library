from typing import List


class Camera:

    """
     Camera settings.
    """
    def __init__(self, selection: List[int] = None, autoExposure: bool = None, exposure: int = None, analogGain: float = None, digitalGain: int = None, focus: int = None):
        # Camera selection.  Default is all cameras.
        self.selection = selection
        # Auto exposure.
        self.autoExposure = autoExposure
        # Exposure.
        self.exposure = exposure
        # Analog gain.
        self.analogGain = analogGain
        # Digital gain.
        self.digitalGain = digitalGain
        # Focus value.
        self.focus = focus


