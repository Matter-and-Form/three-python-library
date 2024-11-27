from typing import List


class NewGroup:

    """
     Scan group settings.
    """
    def __init__(self, parentIndex: int = None, baseName: str = None, color: List[float] = None, visible: bool = None, collapsed: bool = None, rotation: List[float] = None, translation: List[float] = None):
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
        # Group color.
        self.color = color
        # Group visibility.
        self.visible = visible
        # Collapsed state in the group tree.
        self.collapsed = collapsed
        """
        Group axis-angle rotation vector.
        The direction of the vector is the rotation axis.
        The magnitude of the vector is rotation angle in radians.
        """
        self.rotation = rotation
        # Group translation vector.
        self.translation = translation


