from enum import Enum
from typing import List


class ScanSelection:

    """
     Scan selection.
    """
    class Mode(Enum):

        """
         Scan selection mode.
        """
        selected = "selected"  # Select user-selected groups.
        visible = "visible"  # Select visible scans.
        all = "all"  # Select all scans.

    def __init__(self, mode: 'Mode', groups: List[int] = None):
        # The scan selection mode.
        self.mode = mode
        """
        The set of user-selected groups.
        These are only used if the selection mode is 'selected'.
        """
        self.groups = groups


