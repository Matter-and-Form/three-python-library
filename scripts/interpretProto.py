import re
import argparse

from typing import List, Optional, Tuple

class ProtoProperty:
    def __init__(self, type_: str, name: str, optional: bool, comment: str) -> None:
        self.type: str = type_
        self.name: str = name
        self.optional: bool = optional
        self.comment: str = comment

class EnumType:
    def __init__(self, name: str) -> None:
        self.type: str = "enum"
        self.name: str = name
        self.properties: List[ProtoProperty] = []

    def add_property(self, name: str, value: str) -> None:
        self.properties.append(ProtoProperty("enum_value", name, False, f"Value: {value}"))

class MessageType:
    def __init__(self, name: str) -> None:
        self.type: str = "message"
        self.name: str = name
        self.properties: List[ProtoProperty] = []

    def add_property(self, type_: str, name: str, optional: bool, comment: str) -> None:
        self.properties.append(ProtoProperty(type_, name, optional, comment))

def parse_proto(proto_file: str) -> Tuple[List[EnumType], List[MessageType]]:
    with open(proto_file, 'r') as file:
        lines: List[str] = file.readlines()

    enums: List[EnumType] = []
    messages: List[MessageType] = []
    current_message: Optional[MessageType] = None
    current_enum: Optional[EnumType] = None
    in_enum: bool = False
    in_message: bool = False

    for line in lines:
        line = line.strip()

        if line.startswith("enum"):
            in_enum = True
            enum_name: str = re.findall(r'enum (\w+)', line)[0]
            current_enum = EnumType(enum_name)
            enums.append(current_enum)
            continue

        if line.startswith("message"):
            in_message = True
            message_name: str = re.findall(r'message (\w+)', line)[0]
            current_message = MessageType(message_name)
            messages.append(current_message)
            continue

        if in_enum:
            if line == "}":
                in_enum = False
                current_enum = None
            else:
                match = re.findall(r'(\w+) = (\d+);', line)
                if match:
                    name, value = match[0]
                    current_enum.add_property(name, value)

        if in_message:
            if line == "}":
                in_message = False
                current_message = None
            else:
                match = re.findall(r'(\w+) (\w+) = (\d+);', line)
                if match:
                    type_, name, _ = match[0]
                    optional: bool = type_ != "required"
                    comment: str = ""  # Add logic to extract comments if needed
                    current_message.add_property(type_, name, optional, comment)

    return enums, messages

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
    parser = argparse.ArgumentParser(description="Parse a protobuf file and generate Python objects.")
    parser.add_argument('proto_file', type=str, help='Path to the protobuf file')
    args = parser.parse_args()

    enums, messages = parse_proto(args.proto_file)

    for enum in enums:
        print_object(enum)


    for message in messages:
        print_object(message)


if __name__ == "__main__":
    main()