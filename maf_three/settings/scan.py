


from three_api.settings.camera import Camera
from three_api.settings.capture import Capture
from three_api.settings.projector import Projector
from three_api.settings.turntable import Turntable


class Scan:
    def __init__(
            self,
            camera:Camera, 
            capture:Capture,
            projector:Projector,
            turntable: Turntable | None
            ):
        
        self.camera = camera
        self.capture = capture
        self.projector = projector
        self.turntable = turntable

