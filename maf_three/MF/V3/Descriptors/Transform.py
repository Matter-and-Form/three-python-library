from typing import List


class Transform:
    # V3 transform descriptor.
    def __init__(self, rotation: List[float], translation: List[float]):
        """
         Axis-angle rotation vector.
         The direction of the vector is the rotation axis.
         The magnitude of the vector is rotation angle in radians.
        """
        self.rotation = rotation
        # Translation vector.
        self.translation = translation


