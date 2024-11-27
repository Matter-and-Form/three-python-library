class Project:

    """
     Project settings.
    """
    def __init__(self, index: int = None, name: str = None):
        """The index identifying which project the settings applies to.
        If undefined the current open project is used."""
        self.index = index
        # Project name.
        self.name = name


