class Projector:

    """
     Projector settings descriptor.
    """
    class Brightness:

        """
         Projector brightness.
        """
        def __init__(self, value: float, default: float, min: float, max: float):
            self.value = value
            self.default = default
            self.min = min
            self.max = max

    class On:

        """
         Projector on/off.
        """
        def __init__(self, value: bool, default: bool):
            self.value = value
            self.default = default

    def __init__(self, brightness: 'Brightness', on: 'On'):
        # Projector brightness.
        self.brightness = brightness
        # Projector on/off.
        self.on = on


