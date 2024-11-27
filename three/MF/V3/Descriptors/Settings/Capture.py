from MF.V3.Settings.Quality import Quality as MF_V3_Settings_Quality_Quality


class Capture:

    """
     Capture settings descriptor.
    """
    class Quality:

        """
         Capture quality preset.
        """
        def __init__(self, value: MF_V3_Settings_Quality_Quality, default: MF_V3_Settings_Quality_Quality):
            self.value = value
            self.default = default

    class Texture:

        """
         Capture texture.
        """
        def __init__(self, value: bool, default: bool):
            self.value = value
            self.default = default

    class BlendCount:

        """
         Capture image blend count for noise reduction.
        """
        def __init__(self, value: int, default: int, min: int, max: int):
            self.value = value
            self.default = default
            self.min = min
            self.max = max

    class BlendFrequency:

        """
         The starting frequency for which multiple capture images are blended.
        """
        def __init__(self, value: int, default: int, min: int, max: int):
            self.value = value
            self.default = default
            self.min = min
            self.max = max

    def __init__(self, quality: 'Quality', texture: 'Texture', blendCount: 'BlendCount', horizontalBlendFrequency: 'BlendFrequency', verticalBlendFrequency: 'BlendFrequency'):
        # Capture quality preset.
        self.quality = quality
        # Capture texture.
        self.texture = texture
        # Capture blend count.
        self.blendCount = blendCount
        # Starting horizontal blend frequency.
        self.horizontalBlendFrequency = horizontalBlendFrequency
        # Starting vertical blend frequency.
        self.verticalBlendFrequency = verticalBlendFrequency


