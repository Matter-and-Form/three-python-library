from typing import List


class ProtocolInfo:
    """
    Desktop-processing protocol capability descriptor, returned by the
    `GetProtocolInfo` task.  Lets a desktop engine detect what a connected
    scanner supports and degrade gracefully against older firmware.
    """
    def __init__(self, version: int, capabilities: List[str] = None):
        # Desktop-processing protocol version.
        self.version = version
        """
        Capability tokens supported by this server.

        Known capabilities:
        - "scanCaptureStreaming": the server can stream raw scan captures to a
        client for desktop processing (see the `SetProcessingDevices` task
        and the `ScanCapture` descriptor).
        """
        self.capabilities = capabilities


