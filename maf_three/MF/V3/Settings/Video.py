from enum import Enum


class Video:
    # Video settings.
    # Video codecs.
    class Codec(Enum):
        NoCodec = "NoCodec"  # No codec specified.
        RAW = "RAW"  # Raw encoding.
        JPEG = "JPEG"  # JPEG encoding.
        H264 = "H264"  # H264 encoding.

    # Pixel formats.
    class Format(Enum):
        NoFormat = "NoFormat"  # No format specified.
        RGB565 = "RGB565"  # RGB565 16-bit
        RGB888 = "RGB888"  # RGB888 24-bit.
        BGR888 = "BGR888"  # BGR888 24-bit.
        YUV420 = "YUV420"  # YUV 420 planar.

    def __init__(self, codec: 'Codec', format: 'Format', width: int, height: int):
        # Video codec.
        self.codec = codec
        # Pixel format.
        self.format = format
        # Image width.
        self.width = width
        # Image height.
        self.height = height


