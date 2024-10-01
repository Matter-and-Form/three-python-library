class Progress:
    # V3 Task Progress Descriptor
    class ScanProgress:
        # The Scan Progress descriptor
        def __init__(self, current: int, step: str, total: int):
            # The current step of the scan.
            self.current = current
            # The string description of the current step.
            self.step = step
            # The total steps in the progress.
            self.total = total

    def __init__(self, ScanProgress: 'ScanProgress' = None):
        self.ScanProgress = ScanProgress


