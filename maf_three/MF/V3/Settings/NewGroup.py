from typing import List


class NewGroup:
    # Scan group settings.
    def __init__(self, color: List[float], rotation: List[float], translation: List[float], parentIndex: int = None, baseName: str = None, visible: bool = None, collapsed: bool = None):
        # Group color.
        self.color = color
        """
         Group axis-angle rotation vector.
         The direction of the vector is the rotation axis.
         The magnitude of the vector is rotation angle in radians.
        """
        self.rotation = rotation
        # Group translation vector.
        self.translation = translation
        """
         The index of the parent group in which the new group is created.
         If unspecified the new group is added to the root of the group tree.
        """
        self.parentIndex = parentIndex
        """
         Group base name.
         The new group name will start with the base name followed by a unique index number chosen by the backend.
        """
        self.baseName = baseName
        # Group visibility.
        self.visible = visible
        # Collapsed state in the group tree.
        self.collapsed = collapsed


