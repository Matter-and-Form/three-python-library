from typing import List


class Tutorials:

    """
     Tutorials settings descriptor.
    """
    class Show:

        """
         Tutorials to show.
        """
        def __init__(self, value: bool, default: bool):
            self.value = value
            self.default = default

    class Viewed:

        """
         Viewed tutorials.
        """
        class Pages:

            """
             Viewed tutorials pages.
            """
            def __init__(self, value: List[str] = None, default: List[str] = None):
                self.value = value
                self.default = default

        def __init__(self, pages: 'Pages'):
            # Viewed tutorials pages.
            self.pages = pages

    def __init__(self, show: 'Show', viewed: 'Viewed'):
        # Show tutorials.
        self.show = show
        # Viewed tutorials.
        self.viewed = viewed


