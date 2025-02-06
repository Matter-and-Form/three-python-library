from enum import Enum


class Import:

    """
     Import mesh settings.
    """
    class Unit(Enum):

        """
         Unit of imported mesh positions.
        """
        Millimeter = "Millimeter"  # Mesh positions in millimeters.
        Centimeter = "Centimeter"  # Mesh positions in centimeters.
        Meter = "Meter"  # Mesh positions in meters.
        Inch = "Inch"  # Mesh positions in inches.
        Foot = "Foot"  # Mesh positions in feet.

    def __init__(self, name: str = None, scale: float = None, unit: 'Unit' = None, center: bool = None, groupIndex: int = None):
        # Optional name of the impored mesh.  Ignored if the imported file is a zip archive, in which case the archive filenames are used.
        self.name = name
        # Optional scale factor for mesh positions.  Default is 1.0.
        self.scale = scale
        # Unit of imported mesh positions.  Default is millimeters.  Ignored if the scale is specified.
        self.unit = unit
        # If true the mesh is centered at the world origin.  Default is true.
        self.center = center
        # Project group index in which to add the imported meshes.  Default is 0 (root group).
        self.groupIndex = groupIndex


