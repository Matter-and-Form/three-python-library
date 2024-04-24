

from enum import Enum


class Codec(str, Enum):
    # The frames coming from the Scanner are streaming in RAW format.
    RAW = 'RAW',

    # The frames coming from the Scanner are encoded in JPEG format.
    JPEG = 'JPEG',

    # The frames coming from the Scanner are encoded in H264 format.
    H264 = 'H264'


class Format(str, Enum):
    # BGR 24-bit.
    BGR888 = 'RGB888',

    # YUV 420 planar.
    YUV420 = 'YUV420'


class VideoFrameDescriptor:
    def __init__(
            self,
            width = 0,
            height = 0,
            step = 0, 
            number = 0,
            codec = Codec.RAW,
            format = Format.YUV420):
        self.width = width
        self.height = height
        self.step = step
        self.number = number
        self.codec = codec
        self.format = format