from enum import Enum
from typing import List, Dict

class TreeProperty:
    def __init__(self, type_: str, name: str, optional: bool, comment: str, repeated: bool, import_descriptor = None) -> None:
        self.type: str = type_
        self.name: str = name
        self.optional: bool = optional
        self.repeated: bool = repeated
        self.comment: str = comment
        self.import_descriptor: ImportDescriptor = import_descriptor

class TreeProcedure:
    def __init__(self, name: str, request: str, response: str, comment: str) -> None:
        self.name: str = name
        self.request: str = request
        self.response: str = response
        self.comment: str = comment

class NodeType(Enum):
    Class = "Class"
    Enum = "Enum"
    Service = "Service"
    Directory = "Directory"

class TreeNode:
    def __init__(self, name: str, nodeType: NodeType = NodeType.Directory, parent = None, filespace = None):
        self.name = name
        self.type = nodeType
        self.parent = parent
        self.children = {}
        self.properties = []
        self.procedures = []
        self.imports = []
        self.filespace = filespace
        self.comment = None

    def add_child(self, child_node):
        self.children[child_node.name] = child_node
    
    def add_property(self, type_: str, name: str, optional: bool, comment: str, repeated: bool) -> None:
        self.properties.append(TreeProperty(type_, name, optional, comment, repeated))
    
    def add_procedure(self, name: str, request: str, response: str, comment: str) -> None:
        self.procedures.append(TreeProcedure(name, request, response, comment))
    
    def add_import(self, import_path: str):
        self.imports.append(ImportDescriptor(import_path))

    def get_child(self, name: str):
        parts = name.split('.')
        # Check each part of the name to see if it is a child
        temp = self
        while temp and len(parts) > 0:
            temp = temp.children.get(parts[0], None)
            parts = parts[1:]
        if temp:
            return temp
        return None
    
    def has_child(self, name: str):
        temp = self.get_child(name)
        if temp:
            return True
        return False

    def get_path(self):
        path = []
        current_node = self
        while current_node:
            if current_node.name == "root":
                break
            path.append(current_node.name)
            current_node = current_node.parent
        return '.'.join(reversed(path))
    
    def get_relative_path(self, node):
        path = []
        current_node = self
        while current_node != node:
            if current_node.name == "root":
                break
            path.append(current_node.name)
            current_node = current_node.parent
        if current_node:
            path.append(current_node.name)
        return '.'.join(reversed(path))
    
    def get_first_parent_with_name(self, name: str):
        # Break the name into parts
        top_name = name.split('.')[0]

        current_node = self
        while current_node:
            if current_node.name == "root":
                break
            if current_node.name == top_name:
                return current_node
            current_node = current_node.parent
        return None
    
    def climbing_search(self, name: str):
        current_node = self
        #find the top level node and return it's child
        while current_node:
            if current_node.name == "root":
                break
            if current_node.name == name:
                return current_node
            elif current_node.has_child(name):
                return current_node.get_child(name)
            current_node = current_node.parent
        return None
    
class Tree:
    def __init__(self):
        self.root = TreeNode("root")

    def add_path(self, path: str, filespace) -> TreeNode:
        parts = path.split('.')
        current_node = self.root
        for part in parts:
            if part not in current_node.children:
                new_node = TreeNode(part, parent=current_node)
                current_node.add_child(new_node)
            current_node = current_node.get_child(part)
        current_node.filespace = filespace
        return current_node

    def search(self, path: str) -> TreeNode:
        parts = path.split('.')
        current_node = self.root
        for part in parts:
            current_node = current_node.get_child(part)
            if current_node is None:
                return None
        return current_node
    
    def get_nodes_with_filespace(self, filespace: str) -> TreeNode:
        nodes = []
        def get_nodes(node):
            if node.filespace == filespace:
                nodes.append(node)
            for child in node.children.values():
                get_nodes(child)
        get_nodes(self.root)
        return nodes
    
    def get_branches_by_filespace(self) -> Dict[str, List[TreeNode]]:
        """
        Traverse the tree and collect nodes by their filespace.

        Returns:
            Dict[str, List[TreeNode]]: A dictionary where the keys are filespace
            identifiers and the values are lists of TreeNode objects that belong
            to that filespace.
        """
        branch_nodes = {}

        def traverse_for_filespace(node: TreeNode):
            if node.filespace:
                if node.filespace not in branch_nodes:
                    branch_nodes[node.filespace] = []
                branch_nodes[node.filespace].append(node)
            else:
                for child in node.children.values():
                    traverse_for_filespace(child)

        traverse_for_filespace(self.root)

        return branch_nodes
    
class ImportDescriptor:
    def __init__(self, file:str):
        self.file = file
        self.types: List[dict[str,str]] = []
    def add_type(self, type:str, replacement:str):
        # Check to see if the type is already in the list
        for t in self.types:
            if t["type"] == type:
                return
        self.types.append({"type":type, "replacement":replacement})

def get_descriptor_by_name(name: str, descriptors: List[dict]) -> ImportDescriptor:
    for descriptor in descriptors:
        if descriptor.file == name:
            return descriptor
    return None

def get_descriptor_by_partial_name(name, import_descriptors) -> ImportDescriptor:
    for descriptor in import_descriptors:
        # replace any . in name with /
        nameAsPath = name.replace('.', '/')
        # match nameAsPath against the last part of descriptor.file
        if descriptor.file.endswith(nameAsPath):
            return descriptor
    return None