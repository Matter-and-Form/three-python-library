from MF.V3.Descriptors.Settings.Advanced import Advanced as MF_V3_Descriptors_Settings_Advanced_Advanced
from MF.V3.Descriptors.Settings.Camera import Camera as MF_V3_Descriptors_Settings_Camera_Camera
from MF.V3.Descriptors.Settings.Capture import Capture as MF_V3_Descriptors_Settings_Capture_Capture
from MF.V3.Descriptors.Settings.I18n import I18n as MF_V3_Descriptors_Settings_I18n_I18n
from MF.V3.Descriptors.Settings.Projector import Projector as MF_V3_Descriptors_Settings_Projector_Projector
from MF.V3.Descriptors.Settings.Software import Software as MF_V3_Descriptors_Settings_Software_Software
from MF.V3.Descriptors.Settings.Style import Style as MF_V3_Descriptors_Settings_Style_Style
from MF.V3.Descriptors.Settings.Turntable import Turntable as MF_V3_Descriptors_Settings_Turntable_Turntable
from MF.V3.Descriptors.Settings.Tutorials import Tutorials as MF_V3_Descriptors_Settings_Tutorials_Tutorials
from MF.V3.Descriptors.Settings.Viewer import Viewer as MF_V3_Descriptors_Settings_Viewer_Viewer


class Scanner:

    """
     Scanner settings descriptor.
    """
    def __init__(self, advanced: MF_V3_Descriptors_Settings_Advanced_Advanced, camera: MF_V3_Descriptors_Settings_Camera_Camera, capture: MF_V3_Descriptors_Settings_Capture_Capture, projector: MF_V3_Descriptors_Settings_Projector_Projector, i18n: MF_V3_Descriptors_Settings_I18n_I18n, style: MF_V3_Descriptors_Settings_Style_Style, turntable: MF_V3_Descriptors_Settings_Turntable_Turntable, tutorials: MF_V3_Descriptors_Settings_Tutorials_Tutorials, viewer: MF_V3_Descriptors_Settings_Viewer_Viewer, software: MF_V3_Descriptors_Settings_Software_Software):
        # Advanced settings descriptor.
        self.advanced = advanced
        # Camera settings descriptor.
        self.camera = camera
        # Capture settings descriptor.
        self.capture = capture
        # Projector settings descriptor.
        self.projector = projector
        # Internalization setting descriptor.
        self.i18n = i18n
        # Style settings descriptor.
        self.style = style
        # Turntable settings descriptor.
        self.turntable = turntable
        # Tutorials settings descriptor.
        self.tutorials = tutorials
        # Viewer settings descriptor.
        self.viewer = viewer
        # Software settings descriptor.
        self.software = software


