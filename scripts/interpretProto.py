import re
import argparse
import os
import glob
from typing import List, Optional, Tuple

class ProtoProperty:
    def __init__(self, type_: str, name: str, optional: bool, comment: str) -> None:
        self.type: str = type_
        self.name: str = name
        self.optional: bool = optional
        self.comment: str = comment

class EnumType:
    def __init__(self, name: str, comment: str, namespace: str) -> None:
        self.type: str = "enum"
        self.name: str = name
        self.comment: str = comment
        self.namespace: str = namespace
        self.properties: List[ProtoProperty] = []

    def add_property(self, name: str, value: str, comment: str) -> None:
        self.properties.append(ProtoProperty("enum_value", name, False, comment))

class MessageType:
    def __init__(self, name: str, comment: str, namespace: str) -> None:
        self.type: str = "message"
        self.name: str = name
        self.comment: str = comment
        self.namespace: str = namespace
        self.properties: List[ProtoProperty] = []

    def add_property(self, type_: str, name: str, optional: bool, comment: str) -> None:
        self.properties.append(ProtoProperty(type_, name, optional, comment))

def parse_proto(proto_file: str, base_dir: str) -> Tuple[List[str], List[EnumType], List[MessageType]]:
    with open(proto_file, 'r') as file:
        lines: List[str] = file.readlines()

    imports: List[str] = []
    enums: List[EnumType] = []
    messages: List[MessageType] = []
    current_message: Optional[MessageType] = None
    current_enum: Optional[EnumType] = None
    in_enum: bool = False
    in_message: bool = False
    comments: List[str] = []

    # Calculate namespace based on the relative path
    relative_path = os.path.relpath(proto_file, base_dir)
    namespace = os.path.dirname(relative_path).replace(os.sep, '.')

    for line in lines:
        line = line.strip()

        if line.startswith("import"):
            match = re.findall(r'import\s+"([^"]+)";', line)
            if match:
                imports.append(match[0])
            continue

        if line.startswith("//") or line.startswith("/*") or line.startswith("*"):
            comments.append(line)
            continue

        if line == "":
            continue

        if line.startswith("enum"):
            in_enum = True
            enum_name: str = re.findall(r'enum (\w+)', line)[0]
            comment: str = "\n".join(comments)
            current_enum = EnumType(enum_name, comment, namespace)
            enums.append(current_enum)
            comments = []
            continue

        if line.startswith("message"):
            in_message = True
            message_name: str = re.findall(r'message (\w+)', line)[0]
            comment: str = "\n".join(comments)
            current_message = MessageType(message_name, comment, namespace)
            messages.append(current_message)
            comments = []
            continue

        if in_enum:
            if line == "}":
                in_enum = False
                current_enum = None
            else:
                match = re.findall(r'(\w+) = (\d+);', line)
                if match:
                    name, value = match[0]
                    comment: str = "\n".join(comments)
                    current_enum.add_property(name, value, comment)
                    comments = []

        if in_message:
            if line == "}":
                in_message = False
                current_message = None
            else:
                match = re.findall(r'(optional\s+)?([\w\.]+)\s+(\w+)\s*=\s*(\d+);', line)
                if match:
                    optional_str, type_, name, _ = match[0]
                    optional: bool = bool(optional_str)
                    comment: str = "\n".join(comments)
                    current_message.add_property(type_, name, optional, comment)
                    comments = []

    return imports, enums, messages

def print_object(obj: object, indent: int = 0) -> None:
    indent_str = ' ' * indent
    if isinstance(obj, list):
        for item in obj:
            print_object(item, indent)
    elif isinstance(obj, ProtoProperty):
        print(f"{indent_str}{obj.name} ({obj.type}) - Optional: {obj.optional}, Comment: {obj.comment}")
    else:
        print(f"{indent_str}{obj.__class__.__name__}: {obj.name}")
        for key, value in obj.__dict__.items():
            if key != 'name' and key != 'type':
                if isinstance(value, list):
                    print(f"{indent_str}  {key}:")
                    print_object(value, indent + 4)
                else:
                    print(f"{indent_str}  {key}: {value}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a directory of protobuf files and generate Python objects.")
    parser.add_argument('directory', type=str, help='Path to the directory containing protobuf files')
    args = parser.parse_args()

    proto_files = glob.glob(os.path.join(args.directory, '**', '*.proto'), recursive=True)

    for proto_file in proto_files:
        print(f"Parsing file: {proto_file}")
        imports, enums, messages = parse_proto(proto_file, args.directory)

        print("Imports:")
        for imp in imports:
            print(f"  {imp}")

        for enum in enums:
            print_object(enum)

        for message in messages:
            print_object(message)

if __name__ == "__main__":
    main()