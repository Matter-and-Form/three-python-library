from MF.V3.Settings.Software import Software
from typing import List


class System:
    # System descriptor.
    class DiskSpace:
        # Disk space descriptor.
        def __init__(self, capacity: int, available: int):
            # Disk space capacity in bytes.
            self.capacity = capacity
            # Available disk space in bytes.
            self.available = available

    class Software:
        # Software descriptor.
        class Version:
            # Software version descriptor.
            def __init__(self, major: int, minor: int, patch: int, suffix: str, string: str):
                # The major version.
                self.major = major
                # The minor version.
                self.minor = minor
                # The patch version.
                self.patch = patch
                # The alphanumeric suffix. e.g. "rc0"
                self.suffix = suffix
                # The version string. e.g. "1.2.3-rc0"
                self.string = string

        class Package:
            # Software package descriptor.
            def __init__(self, name: Software.Package, version: 'System.Software.Version', changelog: str):
                # The package name.
                self.name = name
                # The package version.
                self.version = version
                # The package changelog.
                self.changelog = changelog

        def __init__(self, installed: List['Package'], available: List['Package'], nightlyIncluded: bool):
            # Installed software versions.
            self.installed = installed
            # Available software versions.
            self.available = available
            # Nightly releases are included.
            self.nightlyIncluded = nightlyIncluded

    def __init__(self, serialNumber: str, diskSpace: 'DiskSpace', software: 'Software', publicKey: str):
        # Serial number;
        self.serialNumber = serialNumber
        # Used and available disk space.
        self.diskSpace = diskSpace
        # Software descriptor.
        self.software = software
        # GPG public key.
        self.publicKey = publicKey


