from typing import List


class Merge:

    """
     Merge descriptor.
    """
    class Mesh:

        """
         Mesh descriptor.
        """
        def __init__(self, name: str, triangles: int, quads: int, positions: int, normals: int, uvs: int, size: int):
            # The mesh name.
            self.name = name
            # Number of mesh triangle faces.
            self.triangles = triangles
            # Number of quad faces.
            self.quads = quads
            # Number of vertex positions.
            self.positions = positions
            # Number of vertex normals.
            self.normals = normals
            # Number of UV coordinates.
            self.uvs = uvs
            # Total mesh size in bytes.
            self.size = size

    def __init__(self, scans: int, textures: int, maxSimplifyCount: int, meshes: List['Mesh'] = None):
        # The number of input scans.
        self.scans = scans
        # The number of input textures.
        self.textures = textures
        # The maximum number of faces for the simplify merge step.
        self.maxSimplifyCount = maxSimplifyCount
        # The set of merged mesh descriptors.
        self.meshes = meshes


