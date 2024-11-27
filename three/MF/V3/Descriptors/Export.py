from MF.V3.Settings.Export import Export as MF_V3_Settings_Export_Export
from enum import Enum
from typing import List


class Export:

    """
     Scan data descriptor.
    """
    class Face(Enum):

        """
         Geometry face types.
        """
        NoFace = "NoFace"  # No faces.
        Point = "Point"  # Point faces.
        Line = "Line"  # Line faces.
        Triangle = "Triangle"  # Triangle faces.
        Quad = "Quad"  # Quad faces.

    class Texture(Enum):

        """
         Texture support types.
        """
        Empty = "None"  # The format does not support textures.
        Single = "Single"  # The format supports a single texture only.
        Multiple = "Multiple"  # The format supports multiple textures.

    def __init__(self, format: MF_V3_Settings_Export_Export.Format, extension: str, description: str, normals: bool, colors: bool, textures: 'Texture', faces: List['Face'] = None):
        # Export format.
        self.format = format
        # Export file extension. e.g. ".ply"
        self.extension = extension
        # Export format description. e.g. "Polygon format"
        self.description = description
        # Vertex normal support.
        self.normals = normals
        # Vertex color support.
        self.colors = colors
        # Texture (UV) support.
        self.textures = textures
        # Types of supported faces.
        self.faces = faces


