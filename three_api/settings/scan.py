


from three_api.settings.camera import Camera
from three_api.settings.capture import Capture
from three_api.settings.projector import Projector


class Scan:
    def __init__(
            self,
            camera:Camera, 
            capture:Capture,
            projector:Projector, 
            ):
        
        self.camera = camera
        self.capture = capture
        self.projector = projector

