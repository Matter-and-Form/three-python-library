from typing import List


class HeatMap:

    """
     Scan heat map settings.
    """
    def __init__(self, sources: List[int] = None, targets: List[int] = None, outlierDistance: float = None):
        # Set of source group indexes.
        self.sources = sources
        # Set of target group indexes.
        self.targets = targets
        # Threshold for which distances are excluded from the statistics in the descriptor.
        self.outlierDistance = outlierDistance


