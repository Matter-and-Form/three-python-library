


from maf_three.settings_manual.camera import Camera
from maf_three.settings_manual.capture import Capture
from maf_three.settings_manual.projector import Projector
from maf_three.settings_manual.turntable import Turntable


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

