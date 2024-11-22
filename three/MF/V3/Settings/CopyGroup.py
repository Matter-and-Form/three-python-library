from typing import List


class CopyGroup:
    # Copy scan group settings.
    def __init__(self, sourceIndexes: List[int] = None, targetIndex: int = None, childPosition: int = None, nameSuffix: str = None):
        # The indexes of the groups to copy.
        self.sourceIndexes = sourceIndexes
        """
         The index of the group into which the source group are copied.
         If unspecified the copied groups are added to the root of the group tree.
        """
        self.targetIndex = targetIndex
        """
         The position among the target group's children where the copied groups are inserted.
         If unspecified the copied groups are appended to the end of the target group's children.
        """
        self.childPosition = childPosition
        """
         Optional name suffix to append to the copied group names.
         If unspecified the names are unchanged.
        """
        self.nameSuffix = nameSuffix


