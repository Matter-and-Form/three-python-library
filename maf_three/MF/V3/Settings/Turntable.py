class Turntable:
    # Turntable settings.
    def __init__(self, scans: int, sweep: int, use: bool = None):
        # The number of turntable scans.
        self.scans = scans
        # Turntable angle sweep in degrees.
        self.sweep = sweep
        # Use the turntable.
        self.use = use


