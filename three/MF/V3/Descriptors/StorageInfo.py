class StorageInfo:
    """
    Storage space of the desktop engine's local workspace and, when a scanner
    is connected, of the scanner.  Returned by the `StorageInfo` task.
    """
    class Space:

        """
         Storage space of one side.
        """
        def __init__(self, available: int, capacity: int):
            # Available bytes.
            self.available = available
            # Total capacity in bytes.
            self.capacity = capacity

    def __init__(self, local: 'Space', scanner: 'Space' = None):
        # The engine's local workspace storage.
        self.local = local
        # The connected scanner's storage.  Absent when no scanner is connected.
        self.scanner = scanner


