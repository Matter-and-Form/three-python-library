class Viewer:

    """
     3D Viewer settings descriptor.
    """
    class TextureOpacity:

        """
         Texture opacity.
        """
        def __init__(self, value: float, default: float, min: float, max: float):
            self.value = value
            self.default = default
            self.min = min
            self.max = max

    def __init__(self, textureOpacity: 'TextureOpacity'):
        # Texture opacity.
        self.textureOpacity = textureOpacity


