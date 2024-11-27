from MF.V3.Settings.ScanSelection import ScanSelection as MF_V3_Settings_ScanSelection_ScanSelection


class BoundingBox:

    """
     Bounding box settings.
    """
    def __init__(self, selection: MF_V3_Settings_ScanSelection_ScanSelection, axisAligned: bool):
        # The scan selection.
        self.selection = selection
        """
        If `true`, align the bounding box with the world axes.
        Otherwise orient the bounding box with the scans.
        """
        self.axisAligned = axisAligned


