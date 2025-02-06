from typing import List


class CopyGroups:

    """
     Copy scan groups settings.
    """
    def __init__(self, sourceIndexes: List[int] = None, targetIndex: int = None, childPosition: int = None, nameSuffix: str = None, enumerate: bool = None):
        # The indexes of the groups to copy.
        self.sourceIndexes = sourceIndexes
        """
        The index of the group into which the source groups are copied.
        If unspecified the copied groups are inserted after their respective source groups within the same parent group.
        """
        self.targetIndex = targetIndex
        """
        The position among the target group's children where the copied groups are inserted.
        If unspecified the copied groups are appended to the end of the target group's children.
        Ignored if the targetIndex is unspecified or specified but does not exist.
        """
        self.childPosition = childPosition
        """
        Optional name suffix to append to the copied group names.
        If unspecified the copied group names are unchanged.
        """
        self.nameSuffix = nameSuffix
        """
        Append a copy index the copied group names. e.g. ("name-2", "name-3").  Default is true.
        If a name suffix is specified then the first copy of each source group is not enumerated,
        but subsequent copies are.
        """
        self.enumerate = enumerate


