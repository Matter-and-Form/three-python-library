class Software:

    """
     Software settings.
    """
    def __init__(self, updateMajor: bool = None, updateNightly: bool = None):
        # Enable major version updates which can have breaking API changes.
        self.updateMajor = updateMajor
        # Enable nightly release candidate updates.
        self.updateNightly = updateNightly


