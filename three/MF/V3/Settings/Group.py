from typing import List


class Group:

    """
     Scan group settings.
    """
    def __init__(self, index: int, name: str = None, color: List[float] = None, visible: bool = None, collapsed: bool = None, rotation: List[float] = None, translation: List[float] = None):
        # The unique group index that identifies the group within the group tree.
        self.index = index
        # Group name.
        self.name = name
        # Color in the renderer.
        self.color = color
        # Visibility in the renderer.
        self.visible = visible
        # Collapsed state in the group tree.
        self.collapsed = collapsed
        """
        Axis-angle rotation vector.
        The direction of the vector is the rotation axis.
        The magnitude of the vector is rotation angle in radians.
        """
        self.rotation = rotation
        # Translation vector.
        self.translation = translation


