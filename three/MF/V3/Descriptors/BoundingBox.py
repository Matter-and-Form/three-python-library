from typing import List


class BoundingBox:

    """
     BoundingBox descriptor.
    """
    def __init__(self, center: List[float] = None, size: List[float] = None, rotation: List[float] = None, transform: List[float] = None):
        # The center of the bounding box.
        self.center = center
        # The size of the bounding box.
        self.size = size
        """
        The 3x3 rotation matrix of the bounding box.
        The first, second and third column vectors are the x, y and z axes of the bounding box.
        """
        self.rotation = rotation
        """
        The 4x4 matrix that transforms the canonical cube with corners [±1, ±1, ±1] to the
        bounding box in world coordinates.
        The transform can be used as the model matrix for rendering the bounding box with an
        OpenGL shader.
        """
        self.transform = transform


