
from enum import Enum

# Video codecs.
class Codec(str, Enum):
    # No codec specified.
    NoCodec = 'NoCodec',
    # Raw encoding.
    RAW = 'RAW',
    # JPEG encoding.
    JPEG = 'JPEG',
    # H264 encoding.
    H264 = 'H264'


 # Pixel formats.
class Format(str, Enum):
    # No format specified.
    NoFormat = 'NoFormat',
    # RGB565 16-bit
    RGB565 = 'RGB565',
    #RGB888 24-bit.
    RGB888 = 'RGB888',
    #BGR888 24-bit.
    BGR888 = 'BGR888',
    #YUV 420 planar.
    YUV420 = 'YUV420'
    

class Video:
    def __init__(
            self,
            width = 0,
            height = 0,
            format = Format.NoFormat,
            codec = Codec.NoCodec):

        self.width = width,
        self.height = height, 
        self.format = format,
        self.codec = codec