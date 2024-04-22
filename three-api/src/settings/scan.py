


from maf.settings.camera import Camera
from maf.settings.capture import Capture
from maf.settings.projector import Projector


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

