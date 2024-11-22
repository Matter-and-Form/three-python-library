class Software:

    """
     Software settings descriptor.
    """
    class UpdateMajor:

        """
         Enable major version updates which can have breaking API changes.
        """
        def __init__(self, value: bool, default: bool):
            self.value = value
            self.default = default

    def __init__(self, updateMajor: 'UpdateMajor'):
        # Enable major version updates which can have breaking API changes.
        self.updateMajor = updateMajor


