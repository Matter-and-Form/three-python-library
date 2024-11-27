class CopyProject:

    """
     Copy project settings.
    """
    def __init__(self, index: int, copyName: str = None):
        # The index of the project to copy.
        self.index = index
        # The name of project copy.  If unspecified a default copy name is generated.
        self.copyName = copyName


