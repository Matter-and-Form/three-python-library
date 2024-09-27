from enum import Enum
from typing import List


class Software:
    # V3 software settings.
    # Software package types.
    class Package(Enum):
        server = "server"  # The server software package.
        frontend = "frontend"  # The frontend software package.

    def __init__(self, installed: List['Package'], available: List['Package'], nightlyIncluded: bool = None):
        # Request installed software packages.  If undefined all installed packages are returned.
        self.installed = installed
        # Request available software packages.  If undefined all available packages are returned.
        self.available = available
        # Permit nightly release upgrades.
        self.nightlyIncluded = nightlyIncluded


