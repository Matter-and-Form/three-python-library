class ScanCapture:
    """
    Raw scan capture image descriptor streamed to clients that process scans
    themselves (`SetProcessingDevices` client processing).  Each stereo capture
    is sent as two buffers, one per camera, described by this descriptor.

    The buffer payload is the raw image data: `rows` rows of `step` bytes,
    pixel format given by the OpenCV type code in `type`.
    """
    def __init__(self, rows: int, cols: int, type: int, step: int, camera: int, focus: int, index: int, orientation: int, frequency: int, phase: int, angle: float, texture: bool):
        # Image rows.
        self.rows = rows
        # Image columns.
        self.cols = cols
        # OpenCV Mat type code (e.g. CV_8UC1).
        self.type = type
        # Row step in bytes.
        self.step = step
        # Camera index (0 or 1).
        self.camera = camera
        # Camera focus.
        self.focus = focus
        # Capture (turntable angle) index.
        self.index = index
        # Pattern orientation, or -1 for texture captures.
        self.orientation = orientation
        # Pattern frequency, or -1 for texture captures.
        self.frequency = frequency
        # Pattern phase, or -1 for texture captures.
        self.phase = phase
        # Turntable angle in radians.
        self.angle = angle
        # True if this is a texture capture.
        self.texture = texture


