class Turntable:

    """
     Turntable settings descriptor.
    """
    class Scans:

        """
         The number of turntable scans.
        """
        def __init__(self, value: int, default: int, min: int, max: int):
            self.value = value
            self.default = default
            self.min = min
            self.max = max

    class Sweep:

        """
         Turntable angle sweep in degrees.
        """
        def __init__(self, value: int, default: int, min: int, max: int):
            self.value = value
            self.default = default
            self.min = min
            self.max = max

    class Use:

        """
         Use the turntable.
        """
        def __init__(self, value: bool, default: bool):
            self.value = value
            self.default = default

    def __init__(self, scans: 'Scans', sweep: 'Sweep', use: 'Use'):
        # The number of turntable scans.
        self.scans = scans
        # Turntable angle sweep in degrees.
        self.sweep = sweep
        # Use the turntable.
        self.use = use


