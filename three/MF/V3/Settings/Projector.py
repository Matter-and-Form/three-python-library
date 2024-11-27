from MF.V3.Settings.Rectangle import Rectangle as MF_V3_Settings_Rectangle_Rectangle
from MF.V3.Settings.Video import Video as MF_V3_Settings_Video_Video
from enum import Enum
from typing import List


class Projector:

    """
     Projector settings.
    """
    class Orientation(Enum):

        """
         Pattern orientation.
        """
        Horizontal = "Horizontal"  # Horizontal pattern.  Image columns are identical.
        Vertical = "Vertical"  # Vertical pattern.  Image rows are identical.

    class Pattern:

        """
         Structured light pattern.
        """
        def __init__(self, orientation: 'Projector.Orientation', frequency: int, phase: int):
            # Pattern orientation.
            self.orientation = orientation
            # Pattern frequency index.  [0 - 8]
            self.frequency = frequency
            # Pattern phase.  [0 - 2]
            self.phase = phase

    class Image:

        """
         Projector image settings
        """
        class Source:

            """
             Image source.
            """
            def __init__(self, format: MF_V3_Settings_Video_Video.Format, width: int, height: int, step: int, fixAspectRatio: bool):
                # Source image format
                self.format = format
                # Source image width.
                self.width = width
                # Source image height.
                self.height = height
                # Source image step in bytes.
                self.step = step
                # Fix the source aspect ratio to the target rectangle.
                self.fixAspectRatio = fixAspectRatio

        def __init__(self, source: 'Source', target: MF_V3_Settings_Rectangle_Rectangle):
            # Image source.
            self.source = source
            # Image target rectangle.
            self.target = target

    def __init__(self, on: bool = None, brightness: float = None, pattern: 'Pattern' = None, image: 'Image' = None, color: List[float] = None):
        # Projector on/off.
        self.on = on
        # Projector brightness.
        self.brightness = brightness
        # Structured light pattern.
        self.pattern = pattern
        # Image to project
        self.image = image
        # Solid color
        self.color = color


