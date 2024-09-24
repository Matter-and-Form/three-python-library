import os
import argparse
from interpretProto import create_proto_objects, MessageType, parse_proto
from typing import List, Dict,Tuple, Set
from enum import Enum
from tree import TreeNode, Tree, TreeProperty, NodeType, ImportDescriptor, get_descriptor_by_partial_filename
import ast
import os
import subprocess

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

python_types = [
    "int", 
    "float", 
    "bool", 
    "str", 
    "bytes"
]
    

def generate_python_code(output_dir: str, tree:Tree) -> set:
    # create a unique set of paths
    paths = set()
      
    branches = tree.get_branches_by_filespace()
    
    for key, branch in branches.items():

        # Get the file path
        file_path = os.path.join(output_dir, key.replace(".", "/") + ".py")
        path =  os.path.dirname(file_path)

        print(f"Parsing file: {file_path}")
                       
        # Create the directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        # Add the path to a unique set
        paths.add(path)
      
        # Generate code for messages
        class_code = ""
        service_code = ""

        class_code = ""
        for node in branch:
            if node.type == NodeType.Class or node.type == NodeType.Enum:
                class_code += generate_class_code(node) + "\n\n"
            # elif node.type == NodeType.Service:
            #     service_code += generate_service_code(node, tree) + "\n\n"
        
        # Get imports    
        imports = get_imports_from_nodes(branch)
        
        import_lines = generate_import_lines(imports)

        # Combine imports, message code, and enum code
        combined_code = import_lines + "\n\n" + class_code + "\n\n" + service_code

        # Write the combined code to a file with the name from the file_path
        with open(file_path, 'w') as f:
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
            module_parts_list.append(ImportDescriptor(module_path, "", ""))
    return module_parts_list

def get_imports_from_nodes(nodes:List[TreeNode]) -> Dict[str, List[ImportDescriptor]]:
    imports = []
    for node in nodes:
        def nested_imports(node) -> List[ImportDescriptor]:
            imports = []
            for imp in node.imports:
                imports.append(imp)
            for prop in node.properties:
                if prop.import_descriptor != None:
                    imports.append(prop.import_descriptor)
            for child in node.children.values():
                imports += nested_imports(child)
            return imports
        
        imports += nested_imports(node)

    # Group import descriptors by their file property
    grouped_imports: Dict[str, List[ImportDescriptor]] = {}
    for imp in imports:
        if imp.file not in grouped_imports:
            grouped_imports[imp.file] = []
        grouped_imports[imp.file].append(imp)

    # Convert the dictionary to a list of lists
    unique_imports = list(grouped_imports.values())
    
    
    return unique_imports

def generate_import_lines(descriptorsLists:Dict[str, List[ImportDescriptor]]) -> str:
    import_lines = []
    
    for descriptors in descriptorsLists:    
        for combined in descriptors.values():
            # If single import, then just add the import line
            # otherwise let's put them all on one line

            for descriptor in combined:
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
                    if descriptor.type == "":
                        import_line = f"import {'.'.join(module_parts[:])}"
                    else:
                        import_line = f"from {'.'.join(module_parts[:])} import {descriptor.type}"
                        if descriptor.replacement != "":
                            import_line += f" as {descriptor.replacement}"
                    import_lines.append(import_line)

    return "\n".join(import_lines)

def get_tree(proto_objects: List)-> Tree:
    tree = Tree()

    # We need to go through the proto_objects twice. 
    # First to build the base tree
   
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

    # Then Loop again to to add the properties to the objects in the tree (self referencing)     
    for obj in proto_objects:
        namespace = obj['namespace']
        for msg in obj['messages']:
            def parse_message_props(message):
                message.path = f"{namespace}.{message.parent + '.' if message.parent else ''}{message.name}"
                node = tree.search(message.path)
                for prop in message.properties:
                    if node.filespace == "MF.V3.Tasks.DownloadProject" and node.name == "Response" and prop.name == "State":
                        print("debug")
                    property = get_property(prop, tree, node, namespace)
                    node.properties.append(property)
                for nested in message.nested_messages:
                    parse_message_props(nested)

            parse_message_props(msg)
        for service in obj['services']:
            service_path = f"{namespace}.{service.name}"
            node = tree.search(service_path)
            for procedure in service.procedures:
                # Remove only the last word from procedure.request and procedure.response
                request_base = procedure.request.rsplit('.', 1)[0]
                response_base = procedure.response.rsplit('.', 1)[0]

                import_descriptor_request = get_descriptor_by_partial_filename(request_base, node.imports)
                import_descriptor_response = get_descriptor_by_partial_filename(response_base, node.imports)

                # Check if the import descriptor is found and throw a message if not
                assert import_descriptor_request != None, f"Descriptor not found for {procedure.request}"
                assert import_descriptor_response != None, f"Descriptor not found for {procedure.response}"

                node.imports.append(ImportDescriptor(import_descriptor_request.file, request_base, ""))
                node.imports.append(ImportDescriptor(import_descriptor_response.file, response_base, ""))
                
                request_node = tree.search(import_descriptor_request.file)
                response_node = tree.search(import_descriptor_response.file)

                # Check if the nodes are valid
                assert request_node != None, f"Node not found for {procedure.request}"
                assert response_node != None, f"Node not found for {procedure.response}"

                assert request_node.has_child("Request"), f"Request node not found for {procedure.request}"
                assert response_node.has_child("Response"), f"Response node not found for {procedure.response}"

                # Add the procedure
                node.add_procedure(procedure.name, request_node.get_child("Request").get_path(), response_node.get_child("Response").get_path(), parseComment(procedure.comment))
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

def get_property(property, tree: Tree, node:TreeNode, message_namespace:str) -> TreeProperty:
    
    tree_property = TreeProperty(property.type, property.name, property.optional, parseComment(property.comment), property.repeated, None)
    if property.type == "TaskState":
        print("debug")

    # 1 Check to see if property is a python type
    if property.type in type_mapping:
        tree_property.type = type_mapping.get(property.type, property.type)
        return tree_property
        
    # 2 Check to see if the property is directly accessible
    import_descriptor = ImportDescriptor(node.filespace, property.type.split(".")[0], "")
    tree_property.import_descriptor = import_descriptor

    direct_node = tree.search(property.type)
    if (direct_node):
        import_descriptor.file = direct_node.filespace
        return tree_property

    # 3 Check to see if the property type is in this file (get root node)
    # - Is it a child of the node?
    if node.has_child(property.type):
        return tree_property
    
    # - Check if the property is a node of a parent
    root_node = node
    while root_node.parent.name != "root":
        root_node = root_node.parent    
        if root_node.has_child(property.type) or root_node.name == property.type:
            property_node = root_node.get_child(property.type)
            import_descriptor.file = property_node.filespace
            return tree_property
    
    # - Check if the property shares a namespace
    property_type_with_namespace = f"{message_namespace}.{property.type}"
    property_node = tree.search(property_type_with_namespace)
    if property_node:
        import_descriptor.file = property_node.filespace
        return tree_property
        
    raise Exception("Property Type could not be resolved", property.type)
    

def generate_class_code(current_node:TreeNode) -> str:

    if current_node.type == NodeType.Enum:
        return generate_enum_code(current_node)

    class_code = f"class {current_node.name}:\n"

    class_code += add_indents(current_node.comment,1)
    if current_node.name == "DownloadProject":
        print("debug")

    # Generate code for nested messages
    for child in current_node.children.values():
        nested_class_code = generate_class_code(child)
        nested_class_code = add_indents(nested_class_code,1)
        class_code += f"\n{nested_class_code}\n"
    
    class_code += "    def __init__(self"
    
    if current_node.properties:
        # sort properties so optionals are last
        properties = sorted(current_node.properties, key=lambda x: x.optional)
        for prop in properties:
            
            prop_type = prop.type
            # Wrap the type in single quotes if it is a self referencing type
            if prop.import_descriptor != None:
                if prop.import_descriptor.file == current_node.filespace:
                    prop_type = f"'{prop.type}'"

            # handle repeated
            if prop.repeated:
                # Get importDescriptor for List "typing"
                
                descriptor = ImportDescriptor("typing", "List", "")
                current_node.imports.append(descriptor)
                class_code += f", {prop.name}:List[{prop_type}]"
            else:
                class_code += f", {prop.name}:{prop_type}"
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
        class_code += "):\n        pass\n"
    
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


def generate_service_code( current_node:TreeNode, tree:Tree) -> str:
    name = current_node.name

    
    service_code = f"class {name}:\n"
    
    service_code += add_indents("_index = 0\n", 1)

    service_code += add_indents(current_node.comment, 1)
    service_code += "    def __init__(self):\n"
    service_code += "        pass\n"
    
    for procedure in current_node.procedures:
        if procedure.name == "update_settings":
            print("Debug")

        request_node = tree.search(procedure.request)
        response_node = tree.search(procedure.response)

        # create a method name from the name value, by adding underscores between camel case
        method_name = ""
        for i, c in enumerate(procedure.name):
            if c.isupper() and i != 0:
               method_name += "_"
            method_name += c.lower()
       
        service_code += f"    def {method_name}(self"
        # loop over all the properties from the request node to get the input node
        
        method_properties = []
        
        # Get the property that has the name Input
        for prop in request_node.properties:
            if prop.name == "Input":
                if prop.import_descriptor != None:
                    current_node.imports.append(prop.import_descriptor)
                    input_node = tree.search(prop.import_descriptor.file)
                    for input_prop in input_node.properties:
                        # Check if the input_prop.type is not a python type
                        if input_prop.type not in python_types:
                            if input_prop.import_descriptor == None:
                                # Remove the single quotes and concat
                                input_prop.type = f"{prop.type}.{input_prop.type}"
                            else:
                                # find the matching type in import descriptor
                                t = [x for x in input_prop.import_descriptor.types if x['type'] == input_prop.type]
                                # if (t[0]['replacement'] != ""):
                                #     t[0]['repl']
                        
                        method_properties.append(input_prop)
                else:
                    method_properties.append(prop)
        
        # Sort the properties so that optionals are last
        method_properties = sorted(method_properties, key=lambda x: x.optional)

        for prop in method_properties:
            service_code += f", {prop.name}:{prop.type}"
            if prop.optional:
                service_code += " = None"
            if prop.import_descriptor != None:
                current_node.imports.append(prop.import_descriptor)

        service_code += f"):\n"
        service_code += add_indents(procedure.comment,2)
        service_code += f"        {method_name}_request = {request_node.parent.name}.{request_node.name}(\n"
        for prop in request_node.properties:
            if prop.name == "Input":
                service_code += f"            {prop.name}={prop.type}(\n"
                for input_prop in method_properties:
                    service_code += f"                {input_prop.name}={input_prop.name},\n"
                service_code += "            ),\n"
            elif prop.name == "Type":
                service_code += f"            {prop.name}=\"{procedure.name}\",\n"
            elif prop.name == "Index":
                service_code += f"            {prop.name}=self._index,\n"
            else:
                service_code += f"            {prop.name}={prop.name},\n"
        service_code += "        )\n"
        # Get the tree for the file
        # parent_node = tree.search(descriptor.file)
        # request_node = parent_node.get_child("Request")
        # response_node = parent_node.get_child("Response")
        
        # if request == None:
        #     request = "Empty"

        
    return service_code

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

def check_undefined_names(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    undefined_names = set()
    defined_names = set()

    class NameVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                if node.id not in defined_names and node.id not in dir(__builtins__):
                    undefined_names.add(node.id)
            elif isinstance(node.ctx, ast.Store):
                defined_names.add(node.id)
            self.generic_visit(node)

    visitor = NameVisitor()
    visitor.visit(tree)

    return undefined_names

def run_flake8(file_path):
    result = subprocess.run(
        ['flake8', '--select=F', file_path],
        capture_output=True, text=True
    )
    return result.stdout

def check_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                # print(f"Running flake8 on {filepath}...")
                flake8_output = run_flake8(filepath)
                if flake8_output:
                    print(f"flake8 issues in {filepath}:\n{flake8_output}")
                # else:
                #     print(f"No flake8 issues in {filepath}")

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
    paths = generate_python_code(args.output_dir, tree)
    generate_init_files(paths, tree, args.output_dir)

    check_files(args.output_dir)


    exit(0)

if __name__ == "__main__":
    main()
    