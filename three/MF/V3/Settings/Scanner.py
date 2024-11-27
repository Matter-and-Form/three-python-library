from MF.V3.Settings.Advanced import Advanced as MF_V3_Settings_Advanced_Advanced
from MF.V3.Settings.Camera import Camera as MF_V3_Settings_Camera_Camera
from MF.V3.Settings.Capture import Capture as MF_V3_Settings_Capture_Capture
from MF.V3.Settings.I18n import I18n as MF_V3_Settings_I18n_I18n
from MF.V3.Settings.Projector import Projector as MF_V3_Settings_Projector_Projector
from MF.V3.Settings.Software import Software as MF_V3_Settings_Software_Software
from MF.V3.Settings.Style import Style as MF_V3_Settings_Style_Style
from MF.V3.Settings.Turntable import Turntable as MF_V3_Settings_Turntable_Turntable
from MF.V3.Settings.Tutorials import Tutorials as MF_V3_Settings_Tutorials_Tutorials
from MF.V3.Settings.Viewer import Viewer as MF_V3_Settings_Viewer_Viewer


class Scanner:

    """
     Scanner settings.
    """
    def __init__(self, advanced: MF_V3_Settings_Advanced_Advanced = None, camera: MF_V3_Settings_Camera_Camera = None, capture: MF_V3_Settings_Capture_Capture = None, i18n: MF_V3_Settings_I18n_I18n = None, projector: MF_V3_Settings_Projector_Projector = None, style: MF_V3_Settings_Style_Style = None, turntable: MF_V3_Settings_Turntable_Turntable = None, tutorials: MF_V3_Settings_Tutorials_Tutorials = None, viewer: MF_V3_Settings_Viewer_Viewer = None, software: MF_V3_Settings_Software_Software = None):
        # Advanced settings.
        self.advanced = advanced
        # Camera settings.
        self.camera = camera
        # Capture settings.
        self.capture = capture
        # I18n settings.
        self.i18n = i18n
        # Projector settings.
        self.projector = projector
        # Style settings.
        self.style = style
        # Turntable settings.
        self.turntable = turntable
        # Tutorials settings.
        self.tutorials = tutorials
        # Viewer settings.
        self.viewer = viewer
        # Software update settings.
        self.software = software


