from typing import List


class Project:
    # V3 project descriptor.
    class Brief:
        # V3 project brief descriptor.
        def __init__(self, index: int, name: str, size: int, modified: List[int]):
            # Project index.
            self.index = index
            # Project name.
            self.name = name
            # Size in bytes.
            self.size = size
            # Project last modified date and time [year, month, day, hour, minute, second].
            self.modified = modified

    class Group:
        # V3 project scan group tree descriptor.
        def __init__(self, index: int, name: str, color: List[float], visible: bool, collapsed: bool, rotation: List[float], translation: List[float], groups: List['Project.Group'], scan: int = None):
            # Group index.
            self.index = index
            # Group name.
            self.name = name
            # Color in the renderer.
            self.color = color
            # Visibility in the renderer.
            self.visible = visible
            # Collapsed state in the group tree.
            self.collapsed = collapsed
            # Axis-angle rotation vector.  The direction of the vector is the rotation axis.  The magnitude of the vector is rotation angle in radians.
            self.rotation = rotation
            # Translation vector.
            self.translation = translation
            # Subgroups.
            self.groups = groups
            # The scan index. If defined this group is a scan and cannot have subgroups.
            self.scan = scan

    def __init__(self, index: int, name: str, groups: 'Group'):
        # Project index.
        self.index = index
        # Project name.
        self.name = name
        self.groups = groups


