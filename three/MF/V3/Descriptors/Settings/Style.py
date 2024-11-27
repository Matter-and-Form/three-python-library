from MF.V3.Settings.Style import Style as MF_V3_Settings_Style_Style


class Style:

    """
     Style settings descriptor.
    """
    class Theme:

        """
         Theme settings descriptor.
        """
        def __init__(self, value: MF_V3_Settings_Style_Style.Theme, default: MF_V3_Settings_Style_Style.Theme):
            self.value = value
            self.default = default

    def __init__(self, theme: 'Theme'):
        # Theme settings descriptor.
        self.theme = theme


