class Image:

    """
     Image descriptor.
    """
    def __init__(self, width: int, height: int, step: int, type: int):
        # Image width.
        self.width = width
        # Image height.
        self.height = height
        # Image row step in bytes.
        self.step = step
        # OpenCV image [type](https:gist.github.com/yangcha/38f2fa630e223a8546f9b48ebbb3e61a).
        self.type = type


