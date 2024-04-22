


from src.settings.camera import Camera
from src.settings.capture import Capture
from src.settings.projector import Projector


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

