import os
import argparse
from interpretProto import create_proto_objects, MessageType, parse_proto
from typing import List, Dict,Tuple, Set
from enum import Enum
from tree import TreeNode, Tree, TreeProperty, NodeType, ImportDescriptor, get_descriptor_by_name, get_descriptor_by_partial_name


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


def generate_python_code(proto_objects: List, output_dir: str, tree:Tree) -> set:
    # create a unique set of paths
    paths = set()
      
    branches = tree.get_branches_by_filespace()
    
    for branch in branches.values():
        # First get imports
        imports = set()
        for node in branch:
            imports.update(node.imports)
        
        code = generate_import_lines(imports)


    for obj in proto_objects:
        print(f"Parsing file: {obj['filename']}")
                
        file_node = tree.search(obj['namespace'])

        # Access namespace, imports, messages, enums from the dictionary obj
        #namespace = obj['namespace']
        imports = obj['imports']
        messages = obj['messages']
        file_path = obj['filename']
        namespace = obj['namespace']
        services = obj['services']

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

        # Generate code for Services
        service_code = ""
        # for service in services:
        #     code = generate_service_code(service, tree, file_node, importDescs)
        #     service_code += code + "\n\n"
            

        # Generate code for messages
        message_code = ""
        for message in messages:
            current_node = file_node.get_child(message.name)
            code = generate_class_code(tree, current_node, importDescs)
            message_code += code + "\n\n"

        # Generate imports another time to get the final output of imports
        import_lines = generate_import_lines(importDescs)

        # Combine imports, message code, and enum code
        combined_code = import_lines + "\n\n" + message_code + "\n\n" + service_code

        # Write the combined code to a file with the name from the file_path
        filename = os.path.join(path, f"{filename}.py")
        with open(filename, 'w') as f:
            f.write(combined_code)
        
    return paths


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

    # We need to go through the proto_objects twice. 
    # First to build the base tree
    # Then to to add the properties to the objects in the tree (self referencing)
    for obj in proto_objects:
        namespace = obj['namespace']
        imports = obj['imports']
        importDescs = get_imports(imports)
        filespace = obj['filename'].replace('/', '.').replace('.proto', '')
        
        if obj['filename'] == "MF/V3/Descriptors/ProjectActions.proto":
            print("Debug")
        for msg in obj['messages']:
            
            def get_nested_messages(message, nested_name_space):   
                # concat message.name with message.parent
                nested_name_space = f"{nested_name_space}.{message.name}"
                #convert filename to namespace 
                node = tree.add_path(nested_name_space, filespace)
                if message.type == "enum":
                    node.type = NodeType.Enum
                elif message.type == "message":
                    node.type = NodeType.Class
                node.imports = importDescs
                node.comment = parseComment(message.comment)
                for nested in message.nested_messages:
                    get_nested_messages(nested, nested_name_space)
            get_nested_messages(msg, namespace)
        for service in obj['services']:
            # I think services are top level definitions, so no parent needed
            service_path = f"{namespace}.{service.name}"
            node = tree.add_path(service_path, filespace)
            node.type = NodeType.Service
            node.imports = importDescs
            node.comment = parseComment(service.comment)
        
    for obj in proto_objects:
        namespace = obj['namespace']
        for msg in obj['messages']:
            def parse_message_props(message):
                message.path = f"{namespace}.{message.parent + '.' if message.parent else ''}{message.name}"
                node = tree.search(message.path)
                for prop in message.properties:
                    prop_type = get_property_type(prop, tree, node, node.imports, namespace)
                    node.add_property(prop_type, prop.name, prop.optional, parseComment(prop.comment), prop.repeated)
                for nested in message.nested_messages:
                    parse_message_props(nested)

            parse_message_props(msg)
    return tree

def parseComment(comment: str) -> str:
    if comment != "":
        if len(comment.split('\n')) > 1:
            class_code = f'"""{comment}"""\n'
        else:
            # remove initial whitespace in comment
            comment = comment.strip()
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
    # if property.type == "Settings.Export" and node.filespace == "MF.V3.Tasks.ExportMerge":
    #     print("Debug")
    
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
        # Make a unique name for the type based on the filespace and the property type
        unique_name = f"{property.type}"
        unique_name = unique_name.replace(".", "_")

        descriptor.add_type(temp.name, unique_name)
        return f"'{unique_name}'"
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
    

def generate_class_code(tree: Tree, current_node:TreeNode, import_descriptors: List[ImportDescriptor]) -> str:

    if current_node.type == NodeType.Enum:
        return generate_enum_code(current_node) + "\n\n"

    properties = current_node.properties
    
    class_code = current_node.comment
    
    class_code += f"class {current_node.name}:\n"

    # Generate code for nested messages
    for child in current_node.children.values():
        nested_class_code = generate_class_code(tree, child, import_descriptors)
        nested_class_code = add_indents(nested_class_code,1)
        class_code += f"\n{nested_class_code}\n"
    
    if properties:
        # sort properties so optionals are last
        properties = sorted(properties, key=lambda x: x.optional)

        class_code += "    def __init__(self"
        for prop in properties:
            

            # handle repeated
            if prop.repeated:
                # Get importDescriptor for List "typing"
                descriptor = get_descriptor_by_name("typing", import_descriptors)
                if descriptor == None:
                    descriptor = ImportDescriptor("typing")
                    import_descriptors.append(descriptor)
                descriptor.add_type("List", "")
                class_code += f", {prop.name}:List[{prop.type}]"
            else:
                class_code += f", {prop.name}:{prop.type}"
            # handle optionals
            if prop.optional:
                class_code += " = None"
        class_code += "):\n"
        for prop in properties:
            # Add comments with spaces
            if prop.comment:
                class_code += f"\n{add_indents(prop.comment,2)}"
            class_code += add_indents(f"self.{prop.name} = {prop.name}\n",2)
    else:
        class_code += "    def __init__(self):\n"
        class_code += "        pass\n"
    
    return class_code

name_mapping = {
    "None": "Empty",
}

def generate_enum_code(enum:TreeNode) -> str:    
    enum_code = enum.comment
    enum_code += f"class {enum.name}(Enum):\n"
    for value in enum.properties:
        name = name_mapping.get(value.name, value.name)
        enum_code += f"    {name} = \"{value.name}\" {value.comment}\n"
    return enum_code

def generate_service_code(service, tree: Tree, current_node:TreeNode, import_descriptors: List[ImportDescriptor]) -> str:
    name = service.name
    procedures = service.procedures
    service_namespace = service.namespace

    class_code = service.comment
    class_code += f"class {name}:\n"
    for procedure in procedures:
        comment = procedure.comment
        name = procedure.name
        request = procedure.request
        response = procedure.response

        descriptor = get_descriptor_by_partial_name(name, import_descriptors, tree)
        # create a method name from the name value, by adding underscores between camel case
        method_name = ""
        for i, c in enumerate(name):
            if c.isupper() and i != 0:
                method_name += "_"
            method_name += c.lower()
        class_code += comment
        
        # Add the descriptor type so that it can be imported
        assert descriptor != None, f"Descriptor not found for {name}"
        descriptor.add_type(name, "")

        # Get the tree for the file
        parent_node = tree.search(descriptor.file)
        request_node = parent_node.get_child("Request")
        response_node = parent_node.get_child("Response")
        
        if request == None:
            request = "Empty"

        
    return class_code

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

    exit(0)

if __name__ == "__main__":
    main()