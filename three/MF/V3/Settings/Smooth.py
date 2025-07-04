from MF.V3.Settings.ScanSelection import ScanSelection as MF_V3_Settings_ScanSelection_ScanSelection


class Smooth:

    """
     Mesh smoothing settings.
    """
    class Taubin:

        """
         Taubin smoothing settings.
        """
        def __init__(self, iterations: int = None, lambda_: float = None, mu: float = None):
            # Number of smoothing iterations.
            self.iterations = iterations
            # First laplacian smoothing filter parameter. Must be greater than zero.
            self.lambda_ = lambda_
            """Second laplacian smoothing filter parameter.
            Must be negative and have magnitude greater or equal to lambda ."""
            self.mu = mu

    def __init__(self, selection: MF_V3_Settings_ScanSelection_ScanSelection = None, taubin: 'Taubin' = None):
        # The scan selection.
        self.selection = selection
        # Taubin smoothing.
        self.taubin = taubin


