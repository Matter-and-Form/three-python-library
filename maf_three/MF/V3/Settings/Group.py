from typing import List


class Group:
    # Scan group settings.
    def __init__(self, index: int, color: List[float], rotation: List[float], translation: List[float], name: str = None, visible: bool = None, collapsed: bool = None):
        # The unique group index that identifies the group within the group tree.
        self.index = index
        # Color in the renderer.
        self.color = color
        """
         Axis-angle rotation vector.
         The direction of the vector is the rotation axis.
         The magnitude of the vector is rotation angle in radians.
        """
        self.rotation = rotation
        # Translation vector.
        self.translation = translation
        # Group name.
        self.name = name
        # Visibility in the renderer.
        self.visible = visible
        # Collapsed state in the group tree.
        self.collapsed = collapsed


