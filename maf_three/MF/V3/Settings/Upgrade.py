class Upgrade:
    # Upgrade settings.
    def __init__(self, majorVersion: bool = None, stable: bool = None):
        # Upgrade major version which can have breaking API changes.
        self.majorVersion = majorVersion
        # Install the latest stable version.
        self.stable = stable


