from MF.V3.Settings.ScanSelection import ScanSelection as MF_V3_Settings_ScanSelection_ScanSelection
from enum import Enum


class Export:
    # Export settings.
    # Scan export formats.
    class Format(Enum):
        ply = "ply"  # Polygon format.
        dae = "dae"  # Digital asset exchange format.
        fbx = "fbx"  # Autodesk format.
        glb = "glb"  # GL transmission format.
        obj = "obj"  # Wavefront format.
        stl = "stl"  # Stereolithography format.
        xyz = "xyz"  # Chemical format.

    def __init__(self, selection: MF_V3_Settings_ScanSelection_ScanSelection = None, texture: bool = None, merge: bool = None, format: 'Format' = None, scale: float = None):
        # The scan selection.
        self.selection = selection
        # Export textures.
        self.texture = texture
        # Merge the scans into a single file.
        self.merge = merge
        # The export format.
        self.format = format
        # Scale factor of the exported geometry.
        self.scale = scale


