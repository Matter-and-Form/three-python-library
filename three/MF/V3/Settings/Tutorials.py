from typing import List


class Tutorials:

    """
     Tutorials settings.
    """
    class Viewed:

        """
         Viewed tutorials.
        """
        def __init__(self, pages: List[str] = None):
            # Viewed tutorials pages.
            self.pages = pages

    def __init__(self, show: bool = None, viewed: 'Viewed' = None):
        # Show tutorials.
        self.show = show
        # Viewed tutorials.
        self.viewed = viewed


