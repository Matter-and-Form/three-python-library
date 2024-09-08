import os
import argparse
from interpretProto import create_proto_objects, MessageType, parse_proto
from typing import List, Dict,Tuple, Set


class TreeNode:
    def __init__(self, name: str, parent = None, filespace = None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.filespace = filespace

    def add_child(self, child_node):
        self.children[child_node.name] = child_node

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

class Tree:
    def __init__(self):
        self.root = TreeNode("root")

    def add_path(self, path: str, filespace):
        parts = path.split('.')
        current_node = self.root
        for part in parts:
            if part not in current_node.children:
                new_node = TreeNode(part, parent=current_node)
                current_node.add_child(new_node)
            current_node = current_node.get_child(part)
        current_node.filespace = filespace

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
    
    def get_node_with_shared_parent(self, reference_node: TreeNode, path: str) -> TreeNode:
        if path == "":
            raise Exception("Path cannot be empty")
        
        parts = path.split('.')
        
        # Go up the tree until we find the node with parts[0]
        current_node = reference_node
        while current_node:
            if current_node.name == parts[0]:
                break
            current_node = current_node.parent
        if current_node == None:
            return None
        
        # Now go down the tree to find the rest of the path
        for part in parts[1:]:
            current_node = current_node.get_child(part)
            if current_node == None:
                return None
        return current_node

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

def load_proto_objects(input_dir: str):
    # Call the function from interpretProto.py to create the proto objects
    proto_objects = create_proto_objects(input_dir)
    return proto_objects

def get_descriptor_by_name(name: str, descriptors: List[dict]) -> ImportDescriptor:
    for descriptor in descriptors:
        if descriptor.file == name:
            return descriptor
    return None

def get_imports(imports: List[str]) -> List[ImportDescriptor]:
    module_parts_list:List[ImportDescriptor] = []

    for imp in imports:
        # Split the import path into parts
        module_path = os.path.splitext(imp.replace('/', '.'))[0]
        # Check module_parts_list for existing module by filename
        foundModule = None
        for module in module_parts_list:
            if module.file == module_path:
                foundModule = module
                break
        if foundModule == None:
            module_parts_list.append(ImportDescriptor(module_path))
    return module_parts_list

def generate_import_lines(descriptors:List[ImportDescriptor]) -> str:
    import_lines = []

    for descriptor in descriptors:
        # Split the import path into parts
        module_path = descriptor.file
        module_parts = module_path.split('.')
        module_name = module_parts[-1]
        
        # Special consideration for google imports and enum
        if "google" in module_parts:
            import_lines.append(f"from {'.'.join(module_parts[:-1])} import {module_name}_pb2 as _{module_name}_pb2")
        elif module_path ==  "enum":
            import_lines.append(f"from enum import Enum")
        else:
            # Go through all the types in the descriptor and add them to the import line
            for type in descriptor.types:
                import_line = f"from {'.'.join(module_parts[:])} import {type['type']}"
                if type['replacement'] != "":
                    import_line += f" as {type['replacement']}"
                import_lines.append(import_line)

    return "\n".join(import_lines)

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
                #convert filename to namespace
                filespace = obj['filename'].replace('/', '.').replace('.proto', '')
                tree.add_path(tree_path, filespace)
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
        namespace = obj['namespace']

        if file_path == "MF/V3/Tasks/UpdateSettings.proto":
            print("Debug")
        # Get the base path of the file
        path = os.path.join(output_dir, os.path.dirname(file_path))

        # Get the filename without the extension
        filename = os.path.basename(file_path).replace('.proto', '')
        
        # Create the directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        # Add the path to a unique set
        paths.add(path)
        
        # Generate imports paths for parsing
        importDescs = get_imports(imports)

        # Generate code for messages
        message_code = ""
        for message in messages:
            current_node = file_node.get_child(message.name)
            if message.type == "message":
                code = generate_message_code(message, tree, current_node, importDescs)
                message_code += code + "\n\n"
            elif message.type == "enum":
                message_code += generate_enum_code(message) + "\n\n"

        # Generate imports another time to get the final output of imports
        import_lines = generate_import_lines(importDescs)

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

def find_remaining_elements_of_b(a_elements, b_elements):
    len_a = len(a_elements)
    len_b = len(b_elements)

    for i in range(len_a):
        if a_elements[i:i+len_b] == b_elements[:len_a-i]:
            return b_elements[len_a-i:]
    return None

def get_property_type(property, tree: Tree, node:TreeNode, import_descriptors: List[ImportDescriptor], message_namespace:str) -> str:
    
    # Check to see if the property type can be mapped to a Python type
    if property.type in type_mapping:
        return type_mapping.get(property.type, property.type)
    

    property_type_parts = property.type.split('.')
    if property.type == "Camera" and node.filespace == "MF.V3.Settings.Scanner":
        print("Debug")
            
    if len(property_type_parts) > 1:
        # Combine message_namespace with property type
        property_type_with_namespace = f"{message_namespace}.{property.type}"
        
        # Try getting the node directly
        property_node = tree.search(property.type)

        # If the property node is not found, try getting the node with the namespace
        if property_node == None:
            property_node = tree.search(property_type_with_namespace)
        
        if property_node == None:
            property_type_with_namespace = f"{message_namespace}.{property.type.split('.')[-1]}"
            property_node = tree.search(property_type_with_namespace)
        
        if property_node == None:
            property_node = node.get_first_parent_with_name(property.type)
            property_node = property_node.parent.get_child(property.type)

        if (property_node.filespace == node.filespace):
            return f"'{property.type}'"
        
        temp = property_node
        while temp.parent.filespace == property_node.filespace:
            temp = temp.parent
        relativePath = property_node.get_relative_path(temp)
        
        descriptor = get_descriptor_by_name(property_node.filespace, import_descriptors)
        descriptor.add_type(temp.name, "")
        return f"'{relativePath}'"
    else:
        
        sibling_nodes = tree.get_nodes_with_filespace(node.filespace)
        for sibling_node in sibling_nodes:
            if sibling_node.has_child(property.type):
                return f"'{property.type}'"
            elif sibling_node.name == property.type:
                return f"'{property.type}'"
        for descriptor in import_descriptors:
            # Search for direct imports first
            descriptor_file_node = tree.search(descriptor.file)
            if descriptor_file_node:
                if descriptor_file_node.name == property.type:
                    descriptor.add_type(property.type, "")
                    return f"'{property.type}'"
        for descriptor in import_descriptors:
            # Search for imports with the same filespace
            descriptor_file_nodes = tree.get_nodes_with_filespace(descriptor.file)
            for descriptor_node in descriptor_file_nodes:
                if descriptor_node == None:
                    continue
                elif descriptor_node.name == property.type:
                    descriptor.add_type(property.type, "")
                    return f"'{property.type}'"
                elif descriptor_node.has_child(property.type):
                    descriptor.add_type(property.type, "")
                    return f"'{property.type}'"
                
        
        print("Debug")
    # Check imports
    tree_nodes = [] 
    for descriptor in import_descriptors:
        tree_nodes.extend(tree.get_nodes_with_filespace(descriptor.file))
    
    tree_nodes.extend(tree.get_nodes_with_filespace(node.filespace))
    
    if node.filespace == "MF.V3.Tasks.UpdateSettings" and property.type == "Descriptors.Settings.Scanner":
        print("Debug")

    for tree_node in tree_nodes:
        tree_parts = tree_node.get_path().split('.')
        remaining_parts = find_remaining_elements_of_b(tree_parts, property_type_parts)
        if remaining_parts == None:
            continue
        elif len(remaining_parts) == 0:
            if (node.filespace == tree_node.filespace):
                return f"'{property.type}'"
            descriptor = get_descriptor_by_name(tree_node.filespace, import_descriptors)
            descriptor.add_type(tree_node.name, "")
            return f"'{property.type}'"
        else:
            child_node = tree_node.get_child(remaining_parts[0])
            if child_node:
                if (node.filespace == child_node.filespace):
                    propName = child_node.get_relative_path(tree_node)
                    return propName
                descriptor = get_descriptor_by_name(tree_node.filespace, import_descriptors)
                descriptor.add_type(tree_node.name, "")
                return f"'{tree_node.name}.{'.'.join(remaining_parts)}'"
            
                
            print("debug")
    print("debug")
    
    
    # Node search down for the property type
    childNode = node.get_child(property.type)
    if childNode:
        return f"'{property.type}'"
    
    

    #run once on imports to see if therre is a direct import
    for tree_node in tree_nodes:
        if tree_node.name == property.type:
            # direct import eg. Rectangle -> MF.V3.Rectangle
            replacementName = tree_node.get_path().replace('.','_')
            # Get descriptor for the import by tree_node filename
            descriptor = get_descriptor_by_name(tree_node.filespace, import_descriptors)
            if descriptor:
                descriptor.add_type(property.type, replacementName)
                return f"'{replacementName}'"

    for tree_node in tree_nodes:
        tree_parts = tree_node.filespace.split('.')
        remaining_parts = find_remaining_elements_of_b(tree_parts, property_type_parts)
        if remaining_parts == None:
            continue

        descriptor = get_descriptor_by_name(tree_node.filespace, import_descriptors)

        if len(remaining_parts) == 0:
            remaining_parts_name = property_type_parts[-1]
            replacementName = tree_node.filespace.replace('.','_')
            if descriptor:
                descriptor.add_type(remaining_parts_name, replacementName)
            else:
                print(f"Descriptor not found for {tree_node.filespace}")
            return f"'{replacementName}'"
        else:
            remaining_parts_name = remaining_parts[0] #'.'.join(property_type_parts[:-len(remaining_parts)])
            replacementName = ""
            if descriptor:
                descriptor.add_type(tree_node.name, replacementName)
            else:
                print(f"Descriptor not found for {tree_node.filespace}")
            if (tree_node.has_child(remaining_parts[0])):
                return f"'{tree_node.name}.{'.'.join(remaining_parts)}'"
            else:
                return f"'{'.'.join(remaining_parts)}'"
        
    # Or Search for siblings
    sibling_node = node.parent.get_child(property.type)
    if sibling_node:
        # while parents share the same filespace, then keep appending the parent name
        parent_node = node
        path = []
        path.append(property.type)
        while parent_node.parent.filespace == sibling_node.filespace:
            parent_node = parent_node.parent
            path.append(parent_node.name)
            
        if node == parent_node:
            return f"'{property.type}'"
        else:
            return f"'{'.'.join(reversed(path))}'"
            

    # Finally Search up the tree for the property type if all else fails
    parent_node = tree.get_node_with_shared_parent(node, property.type)
    if parent_node:
        return f"'{property.type}'"
    
    raise Exception("Property Type could not be resolved", property.type)
    

def generate_message_code(message: Dict, tree: Tree, current_node:TreeNode, import_descriptors: List[ImportDescriptor]) -> str:
    comment = message.comment
    name = message.name
    properties = message.properties
    nested_messages = message.nested_messages
    message_namespace = message.namespace
    
    class_code = parseComment(comment)
    
    class_code += f"class {name}:\n"

    # Generate code for nested messages
    for nested_message in nested_messages:
        nested_class_code = generate_message_code(nested_message, tree, current_node.get_child(nested_message.name), import_descriptors)
        nested_class_code = add_indents(nested_class_code,1)
        class_code += f"\n{nested_class_code}\n"
    
    if properties:
        # sort properties so optionals are last
        properties = sorted(properties, key=lambda x: x.optional)

        class_code += "    def __init__(self"
        for prop in properties:
            
            prop_type = get_property_type(prop, tree, current_node, import_descriptors, message_namespace)

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

    proto_objects = load_proto_objects(args.input_dir)
    paths = generate_python_code(proto_objects, args.output_dir)
    generate_init_files(paths)

if __name__ == "__main__":
    main()