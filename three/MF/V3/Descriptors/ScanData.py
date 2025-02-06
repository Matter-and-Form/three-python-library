from enum import Enum
from typing import List


class ScanData:

    """
     Scan data descriptor.
    """
    class Buffer:

        """
         Scan buffer descriptor.
        """
        class Component:

            """
             Scan buffer component descriptor.
            """
            class Type(Enum):

                """
                 Scan buffer component types.
                """
                Position = "Position"  # Vertex position.
                Normal = "Normal"  # Vertex normal.
                Color = "Color"  # Vertex color.
                UV = "UV"  # Vertex texture coordinate.
                Quality = "Quality"  # Vertex quality.
                Triangle = "Triangle"  # Triangle index.
                Texture = "Texture"  # Texture.

            def __init__(self, type: 'Type', size: int, offset: int, normalized: bool):
                # Scan buffer component type.
                self.type = type
                # Scan buffer component size (ie. the number of elements).
                self.size = size
                """
                Scan buffer component offset.
                This is the starting element for this component at every stride of the buffer.
                """
                self.offset = offset
                # Indicates if the data is normalized.
                self.normalized = normalized

        def __init__(self, stride: int, components: List['Component'] = None):
            # Scan buffer stride.  This should be greater or equal to the sum of the component sizes.
            self.stride = stride
            # Scan buffer components.
            self.components = components

    def __init__(self, index: int, name: str, buffers: List['Buffer'] = None, mean: List[float] = None, stddev: List[float] = None, axisAlignedBoundingBox: List[float] = None):
        # Scan index.
        self.index = index
        # Scan name.
        self.name = name
        # Scan buffer descriptors.
        self.buffers = buffers
        # The mean (centroid) of the vertex positions.
        self.mean = mean
        # The standard deviation of the vertex positions.
        self.stddev = stddev
        # The axis-aligned bounding box of the vertex positions.
        self.axisAlignedBoundingBox = axisAlignedBoundingBox


