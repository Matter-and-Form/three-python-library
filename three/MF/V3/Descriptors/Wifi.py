from typing import List


class Wifi:

    """
     The wifi descriptor.
    """
    class Network:

        """
         The wifi network descriptor.
        """
        def __init__(self, ssid: str, isPublic: bool, isActive: bool, password: str = None, quality: int = None):
            # The service set identifier.
            self.ssid = ssid
            # Is the network public?
            self.isPublic = isPublic
            # Is the network active?
            self.isActive = isActive
            # The network password.
            self.password = password
            # Signal quality [0 ; 100].
            self.quality = quality

    def __init__(self, ssid: str, networks: List['Network'] = None):
        # The wifi ssid.
        self.ssid = ssid
        # The list of wifi networks.
        self.networks = networks


