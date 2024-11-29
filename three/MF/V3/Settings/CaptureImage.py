from enum import Enum
from typing import List


class CaptureImage:

    """
     Capture image settings.
    """
    class Codec(Enum):

        """
         Image codecs.
        """
        jpg = "jpg"  # JPEG encoding.
        png = "png"  # PNG encoding.
        bmp = "bmp"  # Bitmap encoding.
        raw = "raw"  # Raw pixel data (no encoding).

    def __init__(self, selection: List[int] = None, codec: 'Codec' = None, grayscale: bool = None):
        # Camera selection.  Default is all cameras.
        self.selection = selection
        # Image codec.  Default is jpg.
        self.codec = codec
        # Capture 8-bit grayscale image.  Default is false (BGR888).
        self.grayscale = grayscale


