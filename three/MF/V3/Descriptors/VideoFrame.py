from MF.V3.Descriptors.Calibration import DetectedCard as MF_V3_Descriptors_Calibration_DetectedCard
from MF.V3.Settings.Video import Video as MF_V3_Settings_Video_Video


class VideoFrame:

    """
     Video frame descriptor.
    """
    def __init__(self, codec: MF_V3_Settings_Video_Video.Codec, format: MF_V3_Settings_Video_Video.Format, width: int, height: int, step: int, number: int, timestamp: int, duration: int, calibrationCard: MF_V3_Descriptors_Calibration_DetectedCard):
        # Video codec.
        self.codec = codec
        # Pixel format.
        self.format = format
        # Image width.
        self.width = width
        # Image height.
        self.height = height
        # Image row step in bytes.
        self.step = step
        # Frame number.
        self.number = number
        # Frame timestamp.
        self.timestamp = timestamp
        # Frame duration.
        self.duration = duration
        # Calibration card detection.
        self.calibrationCard = calibrationCard


