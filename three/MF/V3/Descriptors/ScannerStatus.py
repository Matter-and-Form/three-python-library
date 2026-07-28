class ScannerStatus:
    """
    The desktop engine's scanner connection status.

    Returned by the `GetScannerStatus` task and pushed to every client as a
    `{"ScannerStatus": {...}}` message whenever the connection state changes.
    """
    def __init__(self, connected: bool, host: str):
        # True if the engine is connected to a scanner.
        self.connected = connected
        # The connected scanner's host name or IP address.  Empty when not connected.
        self.host = host


