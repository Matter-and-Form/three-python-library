class Turntable:

    """
     Turntable settings.
    """
    def __init__(self, scans: int, sweep: int, use: bool = None, pointClippingRadius: float = None, pointClippingMinHeight: float = None, pointClippingMaxHeight: float = None, offsetAngle: float = None):
        # The number of turntable scans.
        self.scans = scans
        # Turntable angle sweep in degrees.
        self.sweep = sweep
        # Use the turntable.
        self.use = use
        # The radius of the point clipping cylinder.
        self.pointClippingRadius = pointClippingRadius
        # The minimum height of the point clipping cylinder.
        self.pointClippingMinHeight = pointClippingMinHeight
        # The maximum height of the point clipping cylinder.
        self.pointClippingMaxHeight = pointClippingMaxHeight
        # The offset Angle of the turntable for starting position
        self.offsetAngle = offsetAngle


