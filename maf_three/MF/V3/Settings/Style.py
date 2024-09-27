from enum import Enum


class Style:
    # Style settings.
    # Themes.
    class Theme(Enum):
        Light = "Light"  # Light mode.
        Dark = "Dark"  # Dark mode.

    def __init__(self, theme: 'Theme' = None):
        # Theme setting.
        self.theme = theme


