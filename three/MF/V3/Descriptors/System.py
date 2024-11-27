class System:

    """
     System descriptor.
    """
    class DiskSpace:

        """
         Disk space descriptor.
        """
        def __init__(self, capacity: int, available: int):
            # Disk space capacity in bytes.
            self.capacity = capacity
            # Available disk space in bytes.
            self.available = available

    def __init__(self, serialNumber: str, diskSpace: 'DiskSpace', publicKey: str):
        # Serial number;
        self.serialNumber = serialNumber
        # Used and available disk space.
        self.diskSpace = diskSpace
        # GPG public key.
        self.publicKey = publicKey


