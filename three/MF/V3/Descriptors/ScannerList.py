from typing import List


class ScannerList:
    """
    Scanners discovered on the local network, returned by the
    `DiscoverScanners` task.
    """
    class Scanner:

        """
         A discovered scanner.
        """
        def __init__(self, name: str, host: str, ip: str, port: int, version: str):
            # The scanner's advertised name (e.g. "THREE").
            self.name = name
            # The scanner's mDNS host name (e.g. "matterandform.local").
            self.host = host
            # The scanner's IPv4 address.
            self.ip = ip
            # The scanner's server port.
            self.port = port
            # The scanner's advertised server version.  Empty if not advertised.
            self.version = version

    def __init__(self, scanners: List['Scanner'] = None):
        # The discovered scanners.
        self.scanners = scanners


