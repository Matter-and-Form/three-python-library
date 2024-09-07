import os
import argparse
from interpretProto import create_proto_objects, MessageType, parse_proto
from typing import List, Dict,Tuple, Set


class TreeNode:
    def __init__(self, name: str, parent = None, object = None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.object = object

    def add_child(self, child_node):
        self.children[child_node.name] = child_node

    def get_child(self, name: str):
        parts = name.split('.')
        return self.children.get(parts[-1], None)
    
    def has_child(self, name: str):
        parts = name.split('.')
        return parts[-1] in self.children

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
    
    def get_first_parent_with_child(self, name: str):
        # Break the name into parts
        parts = name.split('.')
        lastIndex = len(parts) - 1

        current_node = self
        while current_node:
            if parts[-1] in current_node.children:
                return current_node
            current_node = current_node.parent
        return None

class Tree:
    def __init__(self):
        self.root = TreeNode("root")

    def add_path(self, path: str, object):
        parts = path.split('.')
        current_node = self.root
        for part in parts:
            if part not in current_node.children:
                new_node = TreeNode(part, parent=current_node, object=object)
                current_node.add_child(new_node)
            current_node = current_node.get_child(part)

    def search(self, path: str) -> TreeNode:
        parts = path.split('.')
        current_node = self.root
        for part in parts:
            current_node = current_node.get_child(part)
            if current_node is None:
                return None
        return current_node
    
    def partial_search(self, path: str, reference_node: TreeNode) -> TreeNode:
        if path == "":
            raise Exception("Path cannot be empty")
        
        parts = path.split('.')
        current_node = reference_node
        
        if (current_node.name == parts[0]):
            current_node = current_node.parent

        # Check children
        for part in parts:
            current_node = current_node.get_child(part)
            if current_node is None:
                break
        if current_node:
            return current_node
        
        # Check parents
        current_node = reference_node
        while current_node:
            if current_node.name == "root":
                current_node = None
                break
            
            loop_node = current_node
            if current_node.has_child(parts[-1]):
                loop_node = current_node.get_child(parts[-1])
            
            if loop_node.name == parts[-1]:
                index = len(parts) - 1
                temp_node = loop_node
                while index >= 0 and temp_node:
                    if temp_node.name != parts[index]:
                        break
                    index -= 1
                    temp_node = temp_node.parent
                
                if index < 0:
                    return loop_node
            
            current_node = current_node.parent
        
        return None

    def get_shared_parent(self, node1: TreeNode, node2: TreeNode) -> TreeNode:
        path1 = []
        current_node = node1
        while current_node:
            path1.append(current_node)
            current_node = current_node.parent

        path2 = []
        current_node = node2
        while current_node:
            path2.append(current_node)
            current_node = current_node.parent

        shared_parent = None
        while path1 and path2:
            if path1[-1] == path2[-1]:
                shared_parent = path1.pop()
                path2.pop()
            else:
                break
        return shared_parent
    

def load_proto_objects(input_dir: str):
    # Call the function from interpretProto.py to create the proto objects
    proto_objects = create_proto_objects(input_dir)
    return proto_objects

def generate_import_lines(imports: List[str]) -> Tuple[str, Set[str]]:
    import_lines = []
    module_parts_set = set()

    for imp in imports:
        # Split the import path into parts
        module_path = os.path.splitext(imp.replace('/', '.'))[0]
        module_parts = module_path.split('.')
        module_name = module_parts[-1]
        
        # Add module parts to the set
        module_parts_set.add(module_path)

        # Special consideration for google imports and enum
        if "google" in module_parts:
            import_line = f"from {'.'.join(module_parts[:-1])} import {module_name}_pb2 as _{module_name}_pb2"
        elif module_path ==  "enum":
            import_line = f"from enum import Enum"
        else:
            # Check if the import has a namespace
            if len(module_parts) > 1:
                import_line = f"from {'.'.join(module_parts[:])} import *"
            else:
                import_line = f"import {module_path}"
        import_lines.append(import_line)
    return "\n".join(import_lines), module_parts_set

def generate_python_code(proto_objects: List, output_dir: str) -> set:
    # create a unique set of paths
    paths = set()
    
    tree = Tree()
    for obj in proto_objects:
        namespace = obj['namespace']
        for msg in obj['messages']:
            
            def get_nested_messages(message):
                # concat message.name with message.parent
                tree_path = f"{namespace}.{message.parent + '.' if message.parent else ''}{message.name}"
                message.path = tree_path
                tree.add_path(tree_path, message)
                for nested in message.nested_messages:
                    get_nested_messages(nested)
            get_nested_messages(msg)

    for obj in proto_objects:
        print(f"Parsing file: {obj['filename']}")
        
        file_node = tree.search(obj['namespace'])

        # Access namespace, imports, messages, enums from the dictionary obj
        #namespace = obj['namespace']
        imports = obj['imports']
        messages = obj['messages']
        file_path = obj['filename']

        # Get the base path of the file
        path = os.path.join(output_dir, os.path.dirname(file_path))

        # Get the filename without the extension
        filename = os.path.basename(file_path).replace('.proto', '')
        
        # Create the directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        # Add the path to a unique set
        paths.add(path)
        
        # Generate imports
        import_lines, import_paths = generate_import_lines(imports)

        # Generate code for messages
        message_code = ""
        for message in messages:
            current_node = file_node.get_child(message.name)
            if message.type == "message":
                message_code += generate_message_code(message, tree, current_node, import_paths) + "\n\n"
            elif message.type == "enum":
                message_code += generate_enum_code(message) + "\n\n"

        # Combine imports, message code, and enum code
        combined_code = import_lines + "\n\n" + message_code

        # Write the combined code to a file with the name from the file_path
        filename = os.path.join(path, f"{filename}.py")
        with open(filename, 'w') as f:
            f.write(combined_code)
        
    return paths

# Mapping of special types to Python types
type_mapping = {
    "int32": "int",
    "Int32": "int",
    "int64": "int",
    "Int64": "int",
    "uint64": "int",
    "UInt64": "int",
    "uint32": "int",
    "UInt32": "int",
    "bool": "bool",
    "Bool": "bool",
    "float": "float",
    "Float": "float",
    "double": "float",
    "Double": "float",
    "string": "str",
    "String": "str",
    "google.protobuf.Any": "_any_pb2"
}

def parseComment(comment: str) -> str:
    if comment != "":
        if len(comment.split('\n')) > 1:
            class_code = f'"""{comment}"""\n'
        else:
            class_code = f'# {comment}\n'
    else:
        class_code = '\n'
    return class_code

def add_indents(code: str, indent: int) -> str:
    # Indent the code by adding spaces if the line is not empty
    return "\n".join([f"{'    ' * indent}{line}" if line.strip() else line for line in code.split("\n")])

def get_property_type(property, tree: Tree, node:TreeNode, import_paths: Set) -> str:
    
    # Check to see if the property type can be mapped to a Python type
    if property.type in type_mapping:
        return type_mapping.get(property.type, property.type)
    if property.type == "MF.V3.Settings.Scan.Processing.AdaptiveSampling.Type":
        print("stop")

    matching_node = tree.partial_search(property.type, node)
    if matching_node:
        pt = f"'{matching_node.get_path()}'"
        return pt

    for import_path in import_paths:
        import_node = tree.search(import_path)
        if import_node:
            matching_node = tree.partial_search(property.type, import_node)
            if matching_node:
                pt = f"'{matching_node.get_path()}'"
                return pt


    # Check to see if the node has a child with the property type
    if node.has_child(property.type):  
        return f"'{property.type}'"
    
    # Check to see if the property type can be mapped to the tree using imports
    # split the property type into parts
    property_type_parts = property.type.split('.')
    # iterrate through the import paths
    for import_path in import_paths:
        # see if there is a node in the tree that matches the import path
        import_node = tree.search(import_path)
        last_index = len(property_type_parts) - 1
        if import_node:
            if import_node.has_child(property_type_parts[last_index]):
                return f"'{property.type}'"
        # make sure to check the full path
        while import_node and last_index >= 0:
            if import_node.name != property_type_parts[last_index]:
                break
            last_index -= 1
            import_node = import_node.parent
        if last_index == -1:
            return f"'{property.type}'"

    if node.parent.has_child(property.type):
        parts = property.type.split('.')
        return f"'{parts[-1]}'"\

    raise Exception("Property Type could not be resolved", property.type)
    
    # # Check to see if the property type is a direct match to anything the import list
    # elif any(import_path in property.type for import_path in import_paths):
    #     matched_import_path = next(import_path for import_path in import_paths if import_path in property.type)
    #     # Remove the matched import path from the property type, except for its last word
    #     last_word = matched_import_path.split('.')[-1]
    #     prop_type = property.type.replace(matched_import_path, last_word)
    # # Check to see if the property type part of this class
    # elif node.has_child(property.type):
    #     prop_type = f"'{property.type}'"
    # # Check to see if the property type is part of the parent class
    # elif node.parent.has_child(property.type):
    #     parts = property.type.split('.')
    #     prop_type = f"'{parts[-1]}'"\
    # # Otherwise check up the tree.
    # else:
    #     parentWithChild = node.get_first_parent_with_child(property.type)
    #     if parentWithChild:
    #         prop_type = f"'{parentWithChild.get_path()}.{property.type}'"
    #     else:
    #         raise Exception("Property Type could not be resolved", property.type)
        

    return prop_type
def generate_message_code(message: Dict, tree: Tree, current_node:TreeNode, import_paths: Set) -> str:
    comment = message.comment
    name = message.name
    properties = message.properties
    nested_messages = message.nested_messages
    
    class_code = parseComment(comment)
    
    class_code += f"class {name}:\n"
    
    # Generate code for nested messages
    for nested_message in nested_messages:
        nested_class_code = generate_message_code(nested_message, tree, current_node.get_child(nested_message.name), import_paths)
        nested_class_code = add_indents(nested_class_code,1)
        class_code += f"\n{nested_class_code}\n"
    
    if properties:
        # sort properties so optionals are last
        properties = sorted(properties, key=lambda x: x.optional)

        class_code += "    def __init__(self"
        for prop in properties:
            
            prop_type = get_property_type(prop, tree, current_node, import_paths)
            
            # write class init parameter
            class_code += f", {prop.name}: {prop_type}"
            # handle optionals
            if prop.optional:
                class_code += " = None"
        class_code += "):\n"
        for prop in properties:
            # Add comments with parseComment function with spaces
            if prop.comment:
                class_code += f"\n{add_indents(parseComment(prop.comment),2)}"
            class_code += add_indents(f"self.{prop.name} = {prop.name}\n",2)
    else:
        class_code += "    def __init__(self):\n"
        class_code += "        pass\n"
    
    return class_code

def generate_enum_code(enum) -> str:
    comment = enum.comment
    name = enum.name
    values = enum.properties

    enum_code = parseComment(comment)
    enum_code += f"class {name}(Enum):\n"
    for value in values:
        enum_code += f"    {value.name} = \"{value.name}\"  # {value.comment}\n"
    return enum_code

def generate_init_files(paths: set):
    for path in paths:
        init_file = os.path.join(path, "__init__.py")
        with open(init_file, 'w') as f:
            f.write("")
    
def main():
    parser = argparse.ArgumentParser(description="Generate Python classes and enums from protobuf schema objects.")
    parser.add_argument('input_dir', type=str, nargs='?', default='./V3Schema', help='The input directory containing the protobuf schema objects.')
    parser.add_argument('output_dir', type=str, nargs='?', default='./maf_three', help='The output directory to write the generated Python classes and enums.')
    args = parser.parse_args()

    if 1:
        proto_objects = load_proto_objects(args.input_dir)
        paths = generate_python_code(proto_objects, args.output_dir)
        generate_init_files(paths)

    else:
        name = "Descriptors/Calibration.proto" 
        imports, messages, namespace = parse_proto(f"./V3Schema/MF/V3/{name}" , args.input_dir)

        # Add imports enum and messages to an object
        proto_objects = [{
            "imports": imports,
            "messages": messages,
            "namespace": namespace,
            "filename": f"MF/V3/{name}"
        }]
        generate_python_code(proto_objects, args.output_dir)
    

if __name__ == "__main__":
    main()