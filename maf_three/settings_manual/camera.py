


class Camera:
    def __init__(
            self,
            selection = None, 
            autoExposure = None,
            exposure = None, 
            analogGain=None,
            digitalGain=None,
            focus = None):
        
        self.selection = selection
        self.autoExposure = autoExposure
        self.exposure = exposure
        self.analogGain = analogGain
        self.digitalGain = digitalGain
        self.focus = focus
