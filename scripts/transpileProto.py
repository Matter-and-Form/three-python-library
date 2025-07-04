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

reserve_names = {
    "lambda": "lambda_"
}

methods_rename = {
    "import" : "import_file"
}

python_types = [
    "int", 
    "float", 
    "bool", 
    "str", 
    "bytes"
]

required_upload_procedures = [
    "UploadProject",
    "RemoveVertices"
]

optional_upload_procedures = [
    "SetProjector"
]

required_download_procedures = [
    "ScanData",
    "MergeData",
    "Export",
    "ExportMerge",
    "ExportLogs",
    "StartVideo",
    "DepthMap",
    "DownloadProject"
]
    

def generate_python_code(output_dir: str, tree:Tree) -> set:
    """
    Generate Python code from the tree structure.
    This method looks at messages, enums, and services and generates Python code for them.
    Then produces the imports for the files
    Then finally writes the code to the files.
    """
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
            elif node.type == NodeType.Service:
                service_code += generate_service_code(node, tree) + "\n\n"
        
        # Get imports    
        imports = get_imports_from_nodes(branch)
        
        import_lines = generate_import_lines(imports, branch[0].filespace)

        # Combine imports, message code, and enum code
        combined_code = ""
        if (import_lines != ""):
            combined_code = import_lines + "\n\n\n"
        if (class_code != ""):
            combined_code += class_code
        if (service_code != ""):
            combined_code += service_code

        # Write the combined code to a file with the name from the file_path
        with open(file_path, 'w') as f:
            f.write(combined_code)

    return paths

def get_imports_from_nodes(nodes:List[TreeNode]) -> Dict[str, List[ImportDescriptor]]:
    """
    Get the import descriptors from a list of nodes.
    This will also create base descriptors for the properties
    """
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

class ImportList:
    def __init__(self):
        self.file:str = ""
        self.types:List[Dict[str,str]] = []


def generate_import_lines(descriptorsLists:Dict[str, List[ImportDescriptor]], file_path:str) -> str:
    """
    Generate import lines from a list of import descriptors.
    """
    import_lines = []
    
    ImportListArray = []
    for combined in descriptorsLists:    
        importList = ImportList()
        importList.file = combined[0].file
        if (importList.file == file_path):
            continue
        for descriptor in combined:
            importList.types.append({"type":descriptor.type, "replacement":descriptor.replacement})
        ImportListArray.append(importList)

    ImportListArray.sort(key=lambda x: x.file)

    for importList in ImportListArray:

        if importList.file == "enum":
            import_lines.append(f"from enum import Enum")
            continue
        if "google" in importList.file:
            split = importList.file.split('.')
            import_lines.append(f"from {'.'.join(split[:-1])} import {split[-1]}_pb2 as _{split[-1]}_pb2")
            continue

        # remove duplicates from types
        types = {}
        for imp in importList.types:
            if imp["type"] == "":
                continue
            # if types already has the type, check to see if the values will be the same. Throw an error if they are not
            # if imp["type"] in types:
                # if types[imp["type"]] != imp["replacement"]:
                #     raise Exception(f"Type {imp['type']} has multiple replacements {types[imp['type']]} and {imp['replacement']}")
            types[imp["type"]] = imp["replacement"]
        
        # If there are no types, just import the file
        if not types:
            import_lines.append(f"import {importList.file}")
            continue

        import_line = f"from {importList.file} import "
        for i, (t, replacement) in enumerate(types.items()):
            if i > 0:
                import_line += ", "
            import_line += f"{t}"
            if replacement != "":
                import_line += f" as {replacement}"
        import_lines.append(import_line)

    return "\n".join(import_lines)


def get_imports(imports: List[str]) -> List[ImportDescriptor]:
    """
    Get the import descriptors from a list of import paths.
    This is the first step in linking the properties in the tree. 
    """
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

def get_tree(proto_objects: List)-> Tree:
    """ 
    Get's the tree structure of the proto objects
    We use this for a proper reference to the objects that are created afterwards
    """

    tree = Tree()

    # We need to go through the proto_objects twice to build the tree properly. 
    # First to build the base tree without properties
    for obj in proto_objects:
        namespace = obj['namespace']
        imports = obj['imports']
        importDescs = get_imports(imports)
        filespace = obj['filename'].replace('/', '.').replace('.proto', '')
        
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
                node.comment = parseComment(message.comment, False)
                for nested in message.nested_messages:
                    get_nested_messages(nested, nested_name_space)
            get_nested_messages(msg, namespace)
        for service in obj['services']:
            # I think services are top level definitions, so no parent needed
            service_path = f"{namespace}.{service.name}"
            node = tree.add_path(service_path, filespace)
            node.type = NodeType.Service
            node.imports = importDescs
            node.comment = parseComment(service.comment, False)

    # Then Loop again to to add the properties to the objects in the tree (self referencing)     
    for obj in proto_objects:
        namespace = obj['namespace']
        for msg in obj['messages']:
            def parse_message_props(message):
                message.path = f"{namespace}.{message.parent + '.' if message.parent else ''}{message.name}"
                node = tree.search(message.path)
                for prop in message.properties:
                    property = get_property(prop, tree, node, namespace)
                    for key, value in reserve_names.items():
                        if property.name == key:
                            property.name = value
                    node.properties.append(property)
                for nested in message.nested_messages:
                    parse_message_props(nested)

            parse_message_props(msg)
        for service in obj['services']:
            service_path = f"{namespace}.{service.name}"
            node = tree.search(service_path)
            for procedure in service.procedures:

                # Remove only the last word from procedure.request and procedure.response
                request_base = procedure.request.rsplit('.', 2)[-2]
                response_base = procedure.response.rsplit('.', 2)[-2]

                import_descriptor_request = get_descriptor_by_partial_filename(request_base, node.imports)
                import_descriptor_response = get_descriptor_by_partial_filename(response_base, node.imports)

                # Check if the import descriptor is found and throw a message if not
                assert import_descriptor_request != None, f"Descriptor not found for {procedure.request}"
                assert import_descriptor_response != None, f"Descriptor not found for {procedure.response}"
                
                request_root_node = tree.search(import_descriptor_request.file)
                response_root_node = tree.search(import_descriptor_response.file)

                # Check if the nodes are valid. Otherwise we're making some big assumptions
                assert request_root_node != None, f"Node not found for {procedure.request}"
                assert response_root_node != None, f"Node not found for {procedure.response}"

                request_node = request_root_node.get_child("Request")
                response_node = response_root_node.get_child("Response")

                assert request_node, f"Request node not found for {procedure.request}"
                assert response_node, f"Response node not found for {procedure.response}"

                # Add the procedure
                node.add_procedure(procedure.name, request_node, response_node, parseComment(procedure.comment, False), import_descriptor_request, import_descriptor_response)
    return tree

def parseComment(comment: str, property: bool) -> str:
    """
    Simply parse the comment and return it, wrapping multi lines or single lines appropriately
    """
    if comment != "":
        if len(comment.split('\n')) > 1:
            comment_lines = comment.split('\n')
            comment_lines = [line.lstrip() for line in comment_lines]
            comment = '\n'.join(comment_lines)
            comment_code = f'"""{comment}"""\n'
        else:
            if property:
                # remove initial whitespace in comment
                comment = comment.strip()
                comment_code = f'# {comment}\n'
            else:
                comment_code = f'\n"""\n{comment}\n"""\n'
    else:
        return ""
    return comment_code

def add_indents(code: str, indent: int) -> str:
    """
    Add indents to the code
    """
    # Indent the code by adding spaces if the line is not empty
    return "\n".join([f"{'    ' * indent}{line}" if line.strip() else line for line in code.split("\n")])

def get_property(property, tree: Tree, node:TreeNode, message_namespace:str) -> TreeProperty:
    """
    Get the property from the property object. This is complicated as the property could be self referencing, part of the parent class, or from an external import
    """
    tree_property = TreeProperty(property.type, property.name, property.optional, parseComment(property.comment, True), property.repeated, None)

    # 1 Check to see if property is a python type
    if property.type in type_mapping:
        tree_property.type = type_mapping.get(property.type, property.type)
        return tree_property
    
    import_descriptor = ImportDescriptor(node.filespace, property.type.split(".")[-1], "")
    tree_property.import_descriptor = import_descriptor

    # 2 Check to see if the property is directly accessible
    direct_node = tree.search(property.type)
    if (direct_node):
        import_descriptor.file = direct_node.filespace
        relative_path = direct_node.get_relative_path_from_filespace()
        import_descriptor.type = relative_path if relative_path != "" else direct_node.name
        import_descriptor.type = import_descriptor.type.split(".")[0]
        # if import_descriptor.file != node.filespace:
        tree_property.type = relative_path
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
            relative_path = property_node.get_relative_path_from_filespace()
            full_type = relative_path if relative_path != "" else property_node.name
            
            split = full_type.split(".")
            import_descriptor.type = split[0]
            remaining = ".".join(split[1:])

            tree_property.type = full_type
            if import_descriptor.file != node.filespace:
                # replace all . with _ in the type
                import_descriptor.replacement = get_replacement_name( property_node.filespace + "." + import_descriptor.type )
                tree_property.type = import_descriptor.replacement
                if (remaining != ""):
                    tree_property.type += "." + remaining
                
            return tree_property
    
    # - Check if the property shares a namespace
    property_type_with_namespace = f"{message_namespace}.{property.type}"
    property_node = tree.search(property_type_with_namespace)
    if property_node:
        import_descriptor.file = property_node.filespace
        return tree_property
        
    raise Exception("Property Type could not be resolved", property.type)
    

def generate_class_code(current_node:TreeNode) -> str:
    """
    Generate the class code for a node in the tree. This is recursive for children nodes.
    """
    if current_node.type == NodeType.Enum:
        return generate_enum_code(current_node)

    class_code = f"class {current_node.name}:\n"

    class_code += add_indents(current_node.comment,1)
    
    # Generate code for nested messages
    for child in current_node.children.values():
        nested_class_code = generate_class_code(child)
        nested_class_code = add_indents(nested_class_code,1)
        class_code += f"{nested_class_code}\n"
    
    class_code += "    def __init__(self"
    
    if current_node.properties:
        # sort properties so optionals are last
        properties = sorted(current_node.properties, key=lambda x: x.optional)
        # Class init arguments
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
                class_code += f", {prop.name}: List[{prop_type}]"
            else:
                class_code += f", {prop.name}: {prop_type}"
            # handle optionals
            if prop.optional:
                class_code += " = None"
        class_code += "):\n"
        # Internal properties assignment
        for prop in properties:
            # Add comments with spaces
            if prop.comment:
                # TODO Check for types that are not python types and add a isinstance call to cast to that type. This will help unwrapping
                    
                class_code += f"{add_indents(prop.comment,2)}"
            class_code += add_indents(f"self.{prop.name} = {prop.name}\n",2)
    else:
        class_code += "):\n        pass"
    
    return class_code

name_mapping = {
    "None": "Empty",
}

def generate_enum_code(enum:TreeNode) -> str:
    """
    Generate the enum code for a node in the tree.
    """
    enum_code = f"class {enum.name}(Enum):\n"
    enum_code += add_indents(enum.comment,1)
    for value in enum.properties:
        name = name_mapping.get(value.name, value.name)
        enum_code += f"    {name} = \"{value.name}\""
        if value.comment != "":
            enum_code += f"  {value.comment}"
        else:
            enum_code += "\n"
    return enum_code


def get_replacement_name(path:str) -> str:
    return path.replace(".", "_")

def generate_service_code( current_node:TreeNode, tree:Tree) -> str:
    """
    Generate the service code for a node in the tree.
    """
    name = current_node.name

    task_descriptor = get_descriptor_by_partial_filename("Task", current_node.imports)
    if task_descriptor == None:
        task_descriptor = ImportDescriptor("MF.V3", "Task", "")
        current_node.imports.append(task_descriptor)
    task_name = task_descriptor.replacement if task_descriptor.replacement != '' else task_descriptor.type
    
    service_code = ""
      
    for procedure in current_node.procedures:
        
        request_node = procedure.request
        response_node = procedure.response
        
        # create a method name from the name value, by adding underscores between camel case
        method_name = ""
        for i, c in enumerate(procedure.name):
            if c.isupper() and i != 0:
               method_name += "_"
            method_name += c.lower()
        # Replace method_name if it matches any key in defenitions_rename
        method_name = methods_rename.get(method_name, method_name)

        # loop over all the properties from the request node to get the input node
        
        method_properties = []
        # Parse the request properties for convenience to the user
        for prop in request_node.properties:
            if prop.name == "Input":
                if prop.import_descriptor != None:
                    # Get the input node from the tree
                    input_node = tree.search(prop.import_descriptor.file)

                    # Create a new import descriptor because we're going to change the replacement name to avoid conflicts
                    if prop.import_descriptor.replacement == "":
                        prop.import_descriptor.replacement = get_replacement_name(input_node.get_path());
                    prop.type = prop.import_descriptor.replacement
                    # Add the import descriptor to the current node imports
                    current_node.imports.append(prop.import_descriptor)
                    
                    # Loop over the properties of the input node
                    # We need to make the convenience call easier than just the Request itself
                    for input_prop in input_node.properties:
                        # Check if the input_prop.type is not a python type
                        if input_prop.type in python_types:
                            method_properties.append(input_prop)
                            continue;
                        assert(input_prop.import_descriptor != None)
                        if input_prop.import_descriptor != None and input_prop.import_descriptor.replacement == "":
                            import_file_node = tree.search(input_prop.import_descriptor.file)
                            import_node = import_file_node.get_child(input_prop.type)
                            assert(import_node != None)
                            relative_path = import_node.get_relative_path_from_filespace()
                            replacement_name = get_replacement_name(import_file_node.get_path())
                            for imp in current_node.imports:
                                if imp.file == import_node.filespace:
                                    if imp.replacement != "":
                                        replacement_name = imp.replacement
                                
                            new_descriptor = ImportDescriptor(import_node.filespace, relative_path.split(".")[0], replacement_name)
                            
                            #make a new property name by replacing the first part of the relative_path with replacement_name
                            split_relative_path = relative_path.split(".")
                            split_relative_path[0] = replacement_name
                            new_property_name = ".".join(split_relative_path)
                            
                            prop = TreeProperty(new_property_name,input_prop.name, input_prop.optional, input_prop.comment, input_prop.repeated, new_descriptor)
                            method_properties.append(prop)
                            continue;
                        else:
                            assert(input_prop.import_descriptor != None) 
                            method_properties.append(input_prop)
                else:
                    method_properties.append(prop)
        
        
        service_code += f"def {method_name}(self"
        
        # Sort the properties so that optionals are last
        method_properties = sorted(method_properties, key=lambda x: x.optional)

        descriptor = ImportDescriptor("typing", "List", "")
        current_node.imports.append(descriptor)
        
        if procedure.name in required_upload_procedures:
            service_code += ", buffer: bytes"
        
        for prop in method_properties:
            if prop.repeated:
                service_code += f", {prop.name}: List[{prop.type}]"
            else:
                service_code += f", {prop.name}: {prop.type}"
            if prop.optional:
                service_code += " = None"
            if prop.import_descriptor != None:
                current_node.imports.append(prop.import_descriptor)

        if procedure.name in optional_upload_procedures:
            service_code += ", buffer: bytes = None"

        service_code += f") -> {task_name}:\n"
        service_code += add_indents(procedure.comment,1)
        

        def create_object_code(node:TreeNode, postfix:str, ignore_optionals:bool)->str:
            code = ""

            # Get the Request Or Response node from the tree
            filespace_node = tree.search(node.filespace)
            filespace_replacement_name = get_replacement_name(filespace_node.get_path())
            
            # Get the relative path of the node
            rel_path = node.get_relative_path_from_filespace()

            # Replace the first part of the relative path with the replacement name
            split_relative_request_path = rel_path.split(".")
            split_relative_request_path[0] = filespace_replacement_name
            new_request_property_name = ".".join(split_relative_request_path)
            
            # Update the node import_descriptor to have a replacement name
            procedure.request_import.replacement = filespace_replacement_name
            procedure.request_import.type = filespace_node.name

            current_node.imports.append(procedure.request_import)

            code += f"    {method_name}_{postfix} = {new_request_property_name}("
            for i, prop in enumerate(node.properties):
                if (prop.optional and ignore_optionals):
                    continue
                if i>0:
                    code += ","
                code += "\n"        
                if prop.name == "Input":
                    # some property types are python types, so we need to handle them differently
                    if len(method_properties) == 1 and method_properties[0].type in python_types:
                        code += f"        {method_properties[0].name}={method_properties[0].name}"
                    else: # multiple properties will result in a complicated type
                        code += f"        {prop.name}={prop.type}(\n"
                        for input_prop in method_properties:
                            code += f"            {input_prop.name}={input_prop.name},\n"
                        code += "        )"
                elif prop.name == "Type":
                    code += f"        {prop.name}=\"{procedure.name}\""
                elif prop.name == "Index":
                    code += f"        {prop.name}=0"
                else:
                    code += f"        {prop.name}=None"
            code += "\n    )\n"
            return code
        
        
        service_code += create_object_code(request_node, "request", False)
        service_code += create_object_code(response_node, "response", True)
        
    
        service_code += f"    task = {task_name}(Index=0, Type=\"{procedure.name}\", Input={method_name}_request, Output={method_name}_response)\n"
        if procedure.name in required_upload_procedures or procedure.name in optional_upload_procedures:
            service_code += f"    self.SendTask(task, buffer)\n"
        else:
            service_code += f"    self.SendTask(task)\n"
        service_code += f"    return task\n\n\n"

    return service_code

def generate_init_files(paths: set, tree: Tree, output_dir: str):
    """
    Generates init files for use when accessing the classes and enums as a package
    """
    paths.add("./three/MF")
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
        
        sorted_imports = sorted(imports)
       
        with open(init_file, 'w') as f:
            f.write("") #guarantee a file
            for import_path in sorted_imports:
                f.write(f"from {import_path} import * \n")



def transpile(input_dir:str, output_dir:str):
    print("Building python files...")
    # Check to see if input_dir and output_dir contain a trailing slash
    if input_dir[-1] == '/':
        input_dir = input_dir[:-1]
    if output_dir[-1] == '/':
        output_dir = output_dir[:-1]

    proto_objects = create_proto_objects(input_dir)
    tree= get_tree(proto_objects)
    paths = generate_python_code(output_dir, tree)
    generate_init_files(paths, tree, output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Python classes and enums from protobuf schema objects.")
    parser.add_argument('input_dir', type=str, nargs='?', default= './V3Schema', help='The input directory containing the protobuf schema objects.')
    parser.add_argument('output_dir', type=str, nargs='?', default='./three/', help='The output directory to write the generated Python classes and enums.')
    args = parser.parse_args()
    transpile(args.input_dir, args.output_dir)
    exit(0)