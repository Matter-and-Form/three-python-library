class Software:
    # Software settings descriptor.
    class NightlyIncluded:
        # Nightly releases included descriptor.
        def __init__(self, value: bool, default: bool):
            self.value = value
            self.default = default

    def __init__(self, nightlyIncluded: 'NightlyIncluded'):
        # Nightly releases included.
        self.nightlyIncluded = nightlyIncluded


