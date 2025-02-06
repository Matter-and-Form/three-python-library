from MF.V3.Settings.ScanSelection import ScanSelection as MF_V3_Settings_ScanSelection_ScanSelection
from enum import Enum


class Export:

    """
     Export settings.
    """
    class Format(Enum):

        """
         Scan export formats.
        """
        ply = "ply"  # Polygon format.
        dae = "dae"  # Digital asset exchange format.
        fbx = "fbx"  # Autodesk format.
        glb = "glb"  # GL transmission format.
        obj = "obj"  # Wavefront format.
        stl = "stl"  # Stereolithography format.
        xyz = "xyz"  # Chemical format.

    class Color:
        """Settings for mapping the vertex quality to a vertex color.
        The specific meaning of 'quality' depends on the broader context.
        In the case heat maps, the quality is the point-to-mesh distance of the vertex."""
        def __init__(self, scale: float = None, offset: float = None, min: float = None, max: float = None):
            # The scale in `normalizedQuality = quality * scale + offset` that normalizes the quality value to the range [0, 1] which maps to the color range [blue, red] .  `offset` must also be specified.
            self.scale = scale
            # The offset in `normalizedQuality = quality * scale + offset` that normalizes the quality value to the range [0, 1] which maps to the color range [blue, red] .  `scale` must also be specified.
            self.offset = offset
            # The quality value that is mapped to the minimum color (blue).  `max` must also be specified.
            self.min = min
            # The quality value that is mapped to the maximum color (red).   `min` must also be specified.
            self.max = max

    def __init__(self, selection: MF_V3_Settings_ScanSelection_ScanSelection = None, texture: bool = None, merge: bool = None, format: 'Format' = None, scale: float = None, color: 'Color' = None):
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
        self.color = color


