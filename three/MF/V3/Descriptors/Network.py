class Interface:

    """
     Network interface descriptor.
    """
    def __init__(self, name: str, ip: str, ssid: str):
        # The name of the interface.
        self.name = name
        # The address associated with the interface.
        self.ip = ip
        # The ssid or name of the network.
        self.ssid = ssid


