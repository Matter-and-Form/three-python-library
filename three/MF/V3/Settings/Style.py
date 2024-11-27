from enum import Enum


class Style:

    """
     Style settings.
    """
    class Theme(Enum):

        """
         Themes.
        """
        Light = "Light"  # Light mode.
        Dark = "Dark"  # Dark mode.

    def __init__(self, theme: 'Theme' = None):
        # Theme setting.
        self.theme = theme


