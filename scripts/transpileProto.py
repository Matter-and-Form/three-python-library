import os
import argparse
from interpretProto import create_proto_objects, EnumType, MessageType
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
        # Special consideration for google imports
        if "google" in module_parts:
            import_line = f"from {'.'.join(module_parts[:-1])} import {module_name}_pb2 as _{module_name}_pb2"
        else:
            import_line = f"import {module_path}"
        import_lines.append(import_line)
    return "\n".join(import_lines)

def generate_python_code(proto_objects: List, output_dir: str):
    for obj in proto_objects:
        print(obj)
        # Access namespace, imports, messages, enums from the dictionary obj
        #namespace = obj['namespace']
        imports = obj['imports']
        messages = obj['messages']
        enums = obj['enums']
        file_path = obj['filename']

        # Get the base path of the file
        path = os.path.join(output_dir, os.path.dirname(file_path))
        # Get the filename without the extension
        filename = os.path.basename(file_path).replace('.proto', '')
        # Create the directory if it doesn't exist
        os.makedirs(path, exist_ok=True)

        # Generate imports
        import_lines = generate_import_lines(imports)

        # Generate code for messages
        message_code = ""
        for message in messages:
            message_code += generate_message_code(message) + "\n\n"

        # Generate code for enums
        enum_code = ""
        for enum in enums:
            enum_code += generate_enum_code(enum) + "\n\n"

        # Combine imports, message code, and enum code
        combined_code = import_lines + "\n\n" + message_code + enum_code

        # Write the combined code to a file with the name from the file_path
        filename = os.path.join(path, f"{filename}.py")
        with open(filename, 'w') as f:
            f.write(combined_code)

def generate_message_code(message: Dict) -> str:
    comment = message.comment
    name = message.name
    properties = message.properties

    class_code = f'"""{comment}"""\n'
    class_code += f"class {name}:\n"
    class_code += "    def __init__(self"
    for prop in properties:
        class_code += f", {prop.name}: {prop.type}"
        if prop.optional:
            class_code += " = None"
    class_code += "):\n"
    for prop in properties:
        class_code += f"        self.{prop.name} = {prop.name}  # {prop.comment}\n"
    return class_code

def generate_enum_code(enum) -> str:
    comment = enum.comment
    name = enum.name
    values = enum.properties

    enum_code = f'"""{comment}"""\n'
    enum_code += f"from enum import Enum\n\n"
    enum_code += f"class {name}(Enum):\n"
    for value in values:
        enum_code += f"    {value.name} = \"{value.name}\"  # {value.comment}\n"
    return enum_code

def main():
    parser = argparse.ArgumentParser(description="Generate Python classes and enums from protobuf schema objects.")
    parser.add_argument('input_dir', type=str, nargs='?', default='./V3Schema', help='The input directory containing the protobuf schema objects.')
    parser.add_argument('output_dir', type=str, nargs='?', default='./maf_three', help='The output directory to write the generated Python classes and enums.')
    args = parser.parse_args()

    proto_objects = load_proto_objects(args.input_dir)
    generate_python_code(proto_objects, args.output_dir)

if __name__ == "__main__":
    main()