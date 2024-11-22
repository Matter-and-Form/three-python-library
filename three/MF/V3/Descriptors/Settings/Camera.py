from MF.V3.Settings.Rectangle import Rectangle as MF_V3_Settings_Rectangle_Rectangle
from typing import List


class Camera:

    """
     Camera settings descriptor.
    """
    class AutoExposure:

        """
         Auto exposure.
        """
        def __init__(self, value: bool, default: bool):
            self.value = value
            self.default = default

    class Exposure:

        """
         Exposure.
        """
        def __init__(self, value: int, default: int, min: int, max: int):
            self.value = value
            self.default = default
            self.min = min
            self.max = max

    class AnalogGain:

        """
         Analog gain.
        """
        def __init__(self, value: float, default: float, min: float, max: float):
            self.value = value
            self.default = default
            self.min = min
            self.max = max

    class DigitalGain:

        """
         Digital gain.
        """
        def __init__(self, value: int, default: int, min: int, max: int):
            self.value = value
            self.default = default
            self.min = min
            self.max = max

    class Focus:

        """
         Focus settings descriptor.
        """
        class Value:

            """
             Focus value.
            """
            def __init__(self, min: int, max: int, value: List[int] = None, default: List[int] = None):
                self.min = min
                self.max = max
                self.value = value
                self.default = default

        class Box:

            """
             Auto focus box.
            """
            def __init__(self, value: List[MF_V3_Settings_Rectangle_Rectangle] = None, default: List[MF_V3_Settings_Rectangle_Rectangle] = None):
                self.value = value
                self.default = default

        def __init__(self, value: 'Value', box: 'Box'):
            # Focus value.
            self.value = value
            # Auto focus box.
            self.box = box

    def __init__(self, autoExposure: 'AutoExposure', exposure: 'Exposure', analogGain: 'AnalogGain', digitalGain: 'DigitalGain', focus: 'Focus'):
        # Auto exposure.
        self.autoExposure = autoExposure
        # Exposure.
        self.exposure = exposure
        # Analog gain.
        self.analogGain = analogGain
        # Digital gain.
        self.digitalGain = digitalGain
        # Focus settings descriptor.
        self.focus = focus


