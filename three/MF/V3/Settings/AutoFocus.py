from MF.V3.Settings.Rectangle import Rectangle as MF_V3_Settings_Rectangle_Rectangle
from typing import List


class AutoFocus:

    """
     Auto focus settings.
    """
    class Camera:

        """
         Auto focus camera settings.
        """
        def __init__(self, index: int, box: MF_V3_Settings_Rectangle_Rectangle = None):
            # The index of the camera on which to apply auto focus.
            self.index = index
            # The image rectangle in video image pixels on which to apply auto focus.
            self.box = box

    def __init__(self, applyAll: bool, cameras: List['Camera'] = None):
        """
        Apply the final focus value to both cameras.
        This setting is ignored if more than one camera is selected.
        """
        self.applyAll = applyAll
        # The set of cameras on which to apply auto focus.
        self.cameras = cameras


