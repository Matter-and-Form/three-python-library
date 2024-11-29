from MF.V3.Settings.CaptureImage import CaptureImage as MF_V3_Settings_CaptureImage_CaptureImage


class CaptureImage:

    """
     Capture image descriptor.
    """
    def __init__(self, camera: int, codec: MF_V3_Settings_CaptureImage_CaptureImage.Codec, grayscale: bool, width: int, height: int, step: int):
        # The index of the camera that produced the image.
        self.camera = camera
        # Image codec.
        self.codec = codec
        # If true, image is 8-bit grayscale.  Otherwise image is BGR888.
        self.grayscale = grayscale
        # Image width.
        self.width = width
        # Image height.
        self.height = height
        # Image row step in bytes.
        self.step = step


