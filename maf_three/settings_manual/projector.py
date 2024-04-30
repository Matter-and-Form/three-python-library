
from enum import Enum

from maf_three.settings_manual.video import Format

class Orientation(str, Enum):
    # Horizontal pattern.  Image columns are identical.
    Horizontal = 'Horizontal',
    # Vertical pattern.  Image rows are identical.
    Vertical = 'Vertical'

class Pattern:
    def __init__(
            self,
            orientation:Orientation,
            frequency:int,
            phase:int):
        
        self.orientation = orientation
        self.frequency = frequency
        self.phase = phase

class Source:
    def __init__(self, format = Format.NoFormat, width = 0, height = 0, step = 0, fixAspectRatio = True):
        self.format = format
        self.width = width
        self.height = height
        self.step = step
        self.fixAspectRatio = fixAspectRatio


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    

class Image:
    def __init__(
        self,
        source,
        target
    ):
        self.source = source
        self.target = target
        


class Projector:
    def __init__(
            self,
            on = None, 
            brightness = None,
            color = None,

            pattern = None,
            image = None
            ):
        
        self.on = on
        self.brightness = brightness
        self.color = color

        self.pattern = pattern
        self.image = image
        