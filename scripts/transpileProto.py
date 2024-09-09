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

def get_tree(proto_objects: List)-> Tree:
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
    return tree

def generate_python_code(proto_objects: List, output_dir: str, tree:Tree) -> set:
    # create a unique set of paths
    paths = set()

    for obj in proto_objects:
        print(f"Parsing file: {obj['filename']}")
        
        file_node = tree.search(obj['namespace'])

        # Access namespace, imports, messages, enums from the dictionary obj
        #namespace = obj['namespace']
        imports = obj['imports']
        messages = obj['messages']
        file_path = obj['filename']
        namespace = obj['namespace']

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
            code = generate_message_code(message, tree, current_node, importDescs)
            message_code += code + "\n\n"

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

def get_property_type(property, tree: Tree, node:TreeNode, import_descriptors: List[ImportDescriptor], message_namespace:str) -> str:
    
    # Check to see if the property type can be mapped to a Python type
    if property.type in type_mapping:
        return type_mapping.get(property.type, property.type)
    
    property_type_parts = property.type.split('.')
    if property.type == "Settings.Export" and node.filespace == "MF.V3.Tasks.ExportMerge":
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
            property_node = node.climbing_search(property.type)
        
        if property_node == None:
            raise Exception("Property Type could not be resolved", property.type)
        
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
                if sibling_node.parent.name == node.parent.name:
                    #true siblings
                    return f"'{property.type}'"
                else:
                    return f"'{sibling_node.name}.{property.type}'"
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
                
        
    raise Exception("Property Type could not be resolved", property.type)
    

def generate_message_code(message: Dict, tree: Tree, current_node:TreeNode, import_descriptors: List[ImportDescriptor]) -> str:

    if message.type == "enum":
        return generate_enum_code(message) + "\n\n"

    comment = message.comment
    name = message.name
    properties = message.properties
    nested_messages = message.nested_messages
    message_namespace = message.namespace
    
    class_code = parseComment(comment)
    
    class_code += f"class {name}:\n"

    # Generate code for nested messages
    for nested_message in nested_messages:
        if nested_message.type == "enum":
            nested_class_code = generate_enum_code(nested_message) + "\n\n"
        else :
            nested_class_code = generate_message_code(nested_message, tree, current_node.get_child(nested_message.name), import_descriptors)
        nested_class_code = add_indents(nested_class_code,1)
        class_code += f"\n{nested_class_code}\n"
    
    if properties:
        # sort properties so optionals are last
        properties = sorted(properties, key=lambda x: x.optional)

        class_code += "    def __init__(self"
        for prop in properties:
            
            prop_type = get_property_type(prop, tree, current_node, import_descriptors, message_namespace)

            # handle repeated
            if prop.repeated:
                # Get importDescriptor for List "typing"
                descriptor = get_descriptor_by_name("typing", import_descriptors)
                if descriptor == None:
                    descriptor = ImportDescriptor("typing")
                    import_descriptors.append(descriptor)
                descriptor.add_type("List", "")
                class_code += f", {prop.name}:List[{prop_type}]"
            else:
                class_code += f", {prop.name}:{prop_type}"
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

name_mapping = {
    "None": "Empty",
}

def generate_enum_code(enum) -> str:
    comment = enum.comment
    name = enum.name
    values = enum.properties

    enum_code = parseComment(comment)
    enum_code += f"class {name}(Enum):\n"
    for value in values:
        name = name_mapping.get(value.name, value.name)
        enum_code += f"    {name} = \"{value.name}\"  # {value.comment}\n"
    return enum_code

def generate_init_files(paths: set, tree: Tree, output_dir: str):
    for path in paths:
        init_file = os.path.join(path, "__init__.py")
        
        # Remove output_dir from the path
        relative_path = path.replace(output_dir+"/", "")
        relative_path = relative_path.replace("/", ".")
        node = tree.search(relative_path)

        imports:Set[str] = set()

        for child in node.children.values():
            if child.filespace:
                imports.add(child.filespace)

        with open(init_file, 'w') as f:
            f.write("") #guarantee a file
            for import_path in imports:
                f.write(f"from {import_path} import * \n")
    
def main():

    parser = argparse.ArgumentParser(description="Generate Python classes and enums from protobuf schema objects.")
    parser.add_argument('input_dir', type=str, nargs='?', default='./V3Schema', help='The input directory containing the protobuf schema objects.')
    parser.add_argument('output_dir', type=str, nargs='?', default='./maf_three/', help='The output directory to write the generated Python classes and enums.')
    args = parser.parse_args()

    # Check to see if args.input_dir and args.output_dir contain a trailing slash
    if args.input_dir[-1] == '/':
        args.input_dir = args.input_dir[:-1]
    if args.output_dir[-1] == '/':
        args.output_dir = args.output_dir[:-1]

    proto_objects = create_proto_objects(args.input_dir)
    tree= get_tree(proto_objects)
    paths = generate_python_code(proto_objects, args.output_dir, tree)
    generate_init_files(paths, tree, args.output_dir)

if __name__ == "__main__":
    main()