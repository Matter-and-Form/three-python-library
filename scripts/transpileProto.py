import re
import argparse

def parse_proto_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def parse_imports(proto_content):
    import_pattern = r'import\s+"([^"]+)"\s*;'
    imports = re.findall(import_pattern, proto_content)
    return imports

def parse_messages(proto_content):
    message_pattern = r'message\s+(\w+)\s*{([^}]*)}'
    messages = re.findall(message_pattern, proto_content)
    return messages

def parse_enums(proto_content):
    enum_pattern = r'enum\s+(\w+)\s*{([^}]*)}'
    enums = re.findall(enum_pattern, proto_content)
    return enums

def generate_python_class(message_name, message_body):
    class_def = f"class {message_name}:\n"
    class_def += "    def __init__(self"
    
    fields = []
    field_pattern = r'\s*(\w+)\s+(\w+)\s*=\s*\d+\s*;'
    for field_type, field_name in re.findall(field_pattern, message_body):
        fields.append((field_type, field_name))
        class_def += f", {field_name}=None"
    
    class_def += "):\n"
    
    for field_type, field_name in fields:
        class_def += f"        self.{field_name} = {field_name}\n"
    
    return class_def

def generate_python_enum(enum_name, enum_body):
    enum_def = f"class {enum_name}(Enum):\n"
    value_pattern = r'\s*(\w+)\s*=\s*\d+\s*;'
    for value_name in re.findall(value_pattern, enum_body):
        enum_def += f"    {value_name} = '{value_name}'\n"
    return enum_def

def transpile_proto_to_python(proto_file_path, output_file_path):
    proto_content = parse_proto_file(proto_file_path)
    
    imports = parse_imports(proto_content)
    messages = parse_messages(proto_content)
    enums = parse_enums(proto_content)
    
    python_code = "# Generated Python classes from .proto file\n\n"
    python_code += "from enum import Enum\n\n"
    
    for imp in imports:
        python_code += f"# Import: {imp}\n"
    
    for enum_name, enum_body in enums:
        python_code += "\n" + generate_python_enum(enum_name, enum_body) + "\n"
    
    for message_name, message_body in messages:
        python_code += "\n" + generate_python_class(message_name, message_body) + "\n"
    
    with open(output_file_path, 'w') as output_file:
        output_file.write(python_code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transpile a .proto file to a Python file.")
    parser.add_argument("proto_file", help="Path to the input .proto file")
    parser.add_argument("output_file", help="Path to the output .py file")
    
    args = parser.parse_args()
    
    transpile_proto_to_python(args.proto_file, args.output_file)