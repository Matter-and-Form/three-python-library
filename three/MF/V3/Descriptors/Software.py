class Software:

    """
     Software descriptor.
    """
    class Package:

        """
         Software package descriptor.
        """
        def __init__(self, installed: str, update: str, changelog: str):
            # The package installed version.
            self.installed = installed
            # The package update version.  Empty if no update is available.
            self.update = update
            # The package changelog.  Empty if no update is available or the update is a downgrade.
            self.changelog = changelog

    def __init__(self, frontend: 'Package', server: 'Package'):
        # Frontend software package.
        self.frontend = frontend
        # Server software package.
        self.server = server


