import os
import argparse
from interpretProto import create_proto_objects, MessageType, parse_proto
from typing import List, Dict

def load_proto_objects(input_dir: str):
    # Call the function from interpretProto.py to create the proto objects
    proto_objects = create_proto_objects(input_dir)
    return proto_objects

def generate_import_lines(imports: List[str]) -> str:
    import_lines = []
    for imp in imports:
        # Split the import path into parts
        module_path = os.path.splitext(imp.replace('/', '.'))[0]
        module_parts = module_path.split('.')
        module_name = module_parts[-1]
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
    return "\n".join(import_lines)

def generate_python_code(proto_objects: List, output_dir: str) -> set:
    # create a unique set of paths
    paths = set()

    # create a LUT to track the namespaces of each object
    proto_objects_dict = {}
    for obj in proto_objects:
        for msg in obj['messages']:
            
            def get_nested_messages(message):
                proto_objects_dict[message.name] = message.parent
                for nested in message.nested_messages:
                    proto_objects_dict[nested.name] = nested.parent
                    get_nested_messages(nested)
            get_nested_messages(msg)

    for obj in proto_objects:
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
        import_lines = generate_import_lines(imports)

        # Generate code for messages
        message_code = ""
        for message in messages:
            if message.type == "message":
                message_code += generate_message_code(message, proto_objects_dict) + "\n\n"
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

def generate_message_code(message: Dict, proto_objects_dict: Dict) -> str:
    comment = message.comment
    name = message.name
    properties = message.properties
    nested_messages = message.nested_messages
    
    class_code = parseComment(comment)
    
    class_code += f"class {name}:\n"
    
    # Generate code for nested messages
    for nested_message in nested_messages:
        nested_class_code = generate_message_code(nested_message, proto_objects_dict)
        nested_class_code = add_indents(nested_class_code,1)
        class_code += f"\n{nested_class_code}\n"
    
    if properties:
        # sort properties so optionals are last
        properties = sorted(properties, key=lambda x: x.optional)

        class_code += "    def __init__(self"
        for prop in properties:
            #Check to see if the type is in the proto_objects_dict
            if prop.type in proto_objects_dict:
                # Join proto_objects_dict[prop.type] + prop_type
                prop_type = f"'{proto_objects_dict[prop.type]}.{prop.type}'"
            else:
                prop_type = type_mapping.get(prop.type, prop.type)

            
            # Extract the last value of the type if it contains dots
            # if '.' in prop_type:
            #     prop_type = prop_type.split('.')[-1]
            class_code += f", {prop.name}: {prop_type}"
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

    if 0:
        proto_objects = load_proto_objects(args.input_dir)
        paths = generate_python_code(proto_objects, args.output_dir)
        generate_init_files(paths)

    else:
        name = "Descriptors/Settings/Advanced.proto" 
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