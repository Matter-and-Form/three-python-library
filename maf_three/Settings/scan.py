


from maf_three.Settings.camera import Camera
from maf_three.Settings.capture import Capture
from maf_three.Settings.projector import Projector
from maf_three.Settings.turntable import Turntable


class Scan:
    def __init__(
            self,
            camera:Camera, 
            capture:Capture,
            projector:Projector,
            turntable: Turntable | None = None
            ):
        
        self.camera = camera
        self.capture = capture
        self.projector = projector
        self.turntable = turntable

