import re
import argparse
import os
import glob
from typing import List, Optional, Tuple, Set



class ProtoProperty:
    def __init__(self, type_: str, name: str, optional: bool, comment: str) -> None:
        self.type: str = type_
        self.name: str = name
        self.optional: bool = optional
        self.comment: str = comment

class MessageType:
    def __init__(self, type_: str, name: str, comment: str, parent: str) -> None:
        self.type: str = type_
        self.name: str = name
        self.comment: str = comment
        self.properties: List[ProtoProperty] = []
        self.nested_messages = []
        self.parent = parent
        self.path = ""

    def add_property(self, type_: str, name: str, optional: bool, comment: str) -> None:
        self.properties.append(ProtoProperty(type_, name, optional, comment))
    
    def add_nested_message(self, message):
        self.nested_messages.append(message)

def get_parent_name_from_stack(stack: List[MessageType]) -> str:
    if len(stack) == 0:
        return ""
    # Concatinate all the names in the stack with a .
    return ".".join([message.name for message in stack])


def parse_proto(proto_file: str, base_dir: str) -> Tuple[List[str], List[MessageType]]:
    
    with open(proto_file, 'r') as file:
        lines: List[str] = file.readlines()
    
    imports: Set[str] = set()
    messages: List[MessageType] = []
    comments: List[str] = []
    namespace: str = ""
    current_message_stack = []

    for line in lines:
        line = line.strip()

        if line.startswith("package"):
            match = re.findall(r'package\s+([\w\.]+);', line)
            if match:
                namespace = match[0]
            else:
                namespace = ''
            continue

        elif line.startswith("import"):
            match = re.findall(r'import\s+"([^"]+)";', line)
            if match:
                imports.add(match[0])
            continue

        elif line.startswith("//") or line.startswith("/*") or line.startswith("*"):
            cleaned_line = line.lstrip()
            #clean out /* * and // from the comments
            cleaned_line = re.sub(r'^/\*|\*/|^\*|//', '', cleaned_line)
            
            comments.append(cleaned_line)
            continue

        elif line == "":
            continue

        elif line.startswith("message") or line.startswith("enum"):
            comment = "\n".join(comments)

            if line.startswith("enum"):
                message_name = re.findall(r'enum (\w+)', line)[0]
                message_type = "enum"
                imports.add("enum")
            else:
                message_name: str = re.findall(r'message (\w+)', line)[0]
                message_type = "message"
            
            
            parent = get_parent_name_from_stack(current_message_stack)
            new_message = MessageType(message_type, message_name, comment, parent)
            
            if current_message_stack:
                current_message_stack[-1].add_nested_message(new_message)
            else:
                messages.append(new_message)

            current_message_stack.append(new_message)
            
            comments = []
            continue
        elif "proto3" in line or "{" in line:
            continue

        # elif current_message_stack is not empty, then we are in a message
        elif len(current_message_stack) > 0:
            if line == "}":
                current_message_stack.pop()
            else:
                if current_message_stack[-1].type == "enum":
                    match = re.findall(r'(\w+)\s*=\s*(\d+);', line)
                    if match:
                        name, value = match[0]
                        comment = "\n".join(comments)
                        current_message_stack[-1].add_property("string", name, False, comment)
                        comments = []
                    else:
                        print(f"Error parsing enum: {line}")
                else:
                    match = re.findall(r'(optional\s+)?([\w\.]+)\s+(\w+)\s*=\s*(\d+);', line)
                    if match:
                        optional_str, type_, name, _ = match[0]
                        optional: bool = bool(optional_str)
                        comment: str = "\n".join(comments)
                        current_message_stack[-1].add_property(type_, name, optional, comment)
                        comments = []
                    else :
                        print(f"Error parsing message: {line}")
        else:
            print(f"Error parsing line: {line}")

    return imports, messages, namespace

def create_proto_objects(directory: str):
    proto_files = glob.glob(os.path.join(directory, '**', '*.proto'), recursive=True)
    all_objs = []

    for proto_file in proto_files:
        imports, messages, namespace = parse_proto(proto_file, directory)
        # Get relative path of the file
        proto_file = os.path.relpath(proto_file, directory)

        # create object that has imports, and messages, and namespace to keep them together
        all_objs.append({
            "imports": imports,
            "messages": messages,
            "namespace": namespace,
            "filename": proto_file
        })
    return all_objs

# def main() -> None:
#     parser = argparse.ArgumentParser(description="Parse a directory of protobuf files and generate Python objects.")
#     parser.add_argument('directory', type=str, help='Path to the directory containing protobuf files')
#     args = parser.parse_args()
#
#     proto_files = glob.glob(os.path.join(args.directory, '**', '*.proto'), recursive=True)
#
#     for proto_file in proto_files:
#         print(f"Parsing file: {proto_file}")
#         imports, enums, messages = parse_proto(proto_file, args.directory)
#
#         print("Imports:")
#         for imp in imports:
#             print(f"  {imp}")
#
#         for enum in enums:
#             print_object(enum)
#
#         for message in messages:
#             print_object(message)
#
# if __name__ == "__main__":
#     main()