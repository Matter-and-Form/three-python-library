import inspect
import importlib
import ast
import argparse
from collections import defaultdict


def add_indents(code: str, indent: int) -> str:
    """
    Add indents to the code
    """
    # Indent the code by adding spaces if the line is not empty
    return "\n".join([f"{'    ' * indent}{line}" if line.strip() else line for line in code.split("\n")])

def process_annotation(annotation):
    new_imports = {}
    if isinstance(annotation, str):
        # Leave string annotations as is
        new_annotation = annotation
    elif hasattr(annotation, '__origin__') and annotation.__origin__ is not None:
        # Handle generic types
        origin, args = annotation.__origin__, annotation.__args__
        new_origin, origin_imports = process_annotation(origin)
        new_imports.update(origin_imports)
        new_args = []
        for arg in args:
            new_arg, arg_imports = process_annotation(arg)
            new_imports.update(arg_imports)
            new_args.append(new_arg)
        args_str = ', '.join(new_args)
        new_annotation = f'{new_origin}[{args_str}]'
    elif hasattr(annotation, '__module__') and hasattr(annotation, '__name__'):
        # Handle regular types
        module_path, qualname = annotation.__module__, annotation.__qualname__
        if module_path != 'builtins':
            top_level_class = qualname.split('.')[0]
            new_imports[module_path] = top_level_class
        new_annotation = qualname
    else:
        # Fallback for other cases
        new_annotation = str(annotation)
    return new_annotation, new_imports

def generate_py(scanner_module_name, three_module_name, output_file):
    print("Generating .py file...")
    # Import the modules
    three_module = importlib.import_module(three_module_name)
    scanner_module = importlib.import_module(scanner_module_name)

    # Get the class from scanner.py
    scanner_class = getattr(scanner_module, 'Scanner')
 
    # Read the source code of the scanner module
    with open(scanner_module.__file__, 'r') as file:
        scanner_source = file.read()
    
    # Split the source code into comments, and the rest of the code
    scanner_comments = []
    scanner_class = []
    scanner_imports = []
    in_comments = True

    for line in scanner_source.split('\n'):
        stripped_line = line.strip()
        if in_comments and (stripped_line.startswith('#') or not stripped_line):
            scanner_comments.append(line)
        else:
            in_comments = False
            if stripped_line.startswith('import') or stripped_line.startswith('from'):
                scanner_imports.append(line)
                continue
            else:
                scanner_class.append(line)

    # Get the functions from three.py
    three_imports = defaultdict(set)
    # Add THREE to the imports
    three_imports["MF.V3"] = {'Three'}

    three_content = []
    three_functions = inspect.getmembers(three_module, inspect.isfunction)

    # Strip the absolute references from the function names
    for name, func in three_functions:
        new_annotations = {}
        for param_name, annotation in func.__annotations__.items():
            new_annotation, annotation_imports = process_annotation(annotation)
            for module_path, imported_name in annotation_imports.items():
                three_imports[module_path].add(imported_name)
            new_annotations[param_name] = new_annotation
        func.__annotations__ = new_annotations

        # Get the signature and update it with new annotations
        signature = inspect.signature(func)
        parameters = []
        for param in signature.parameters.values():
            # Update the annotation of each parameter
            new_annotation = func.__annotations__.get(param.name, param.annotation)
            new_param = param.replace(annotation=new_annotation)
            parameters.append(new_param)

        # Update the return annotation
        return_annotation = func.__annotations__.get('return', signature.return_annotation)

        # Create a new signature with updated parameters and return annotation
        new_signature = signature.replace(parameters=parameters, return_annotation=return_annotation)
        func.__signature__ = new_signature

        # Add the function signature to the three_content
        three_content.append(f"    def {name}{new_signature}:")
        doc = inspect.getdoc(func)
        if doc:
            three_content.append(f'        """{doc}"""')

        # Construct the parameter string for the function call
        param_names = ', '.join(param.name for param in parameters)
        three_content.append(f"        return Three.{name}({param_names})")
        three_content.append("")

    # Start generating the .py content
    scanner_content = []

    # Add Warning
    scanner_content.append("# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    scanner_content.append("# This file is Auto Generated by generateScannerPy.py. Do not edit this file manually.")
    scanner_content.append("# Modifications should be made to _scanner.py and then run generateScannerPy.py to update this file.")
    scanner_content.append("# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    scanner_content.append("")

    # Add comments
    scanner_content.extend(scanner_comments)

    # Add imports from three_imports dictionary
    for module_path, imported_names in three_imports.items():
        imports = ', '.join(imported_names)
        scanner_content.append(f"from {module_path} import {imports}")

    # Add Scanner imports
    scanner_content.append("")
    scanner_content.extend(scanner_imports)
    
    # add the rest of the code
    scanner_content.extend(scanner_class)

    #now add the three functions    
    scanner_content.append("")
    scanner_content.append("    # Dynamically bound functions from three.py")
    scanner_content.append("")    

    scanner_content.extend(three_content)
    
    # Write to the output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(scanner_content))
    print("Completed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a scanner.py file with dynamic functions from three.")
    parser.add_argument('scanner_module', type=str, nargs='?', default='three._scanner', help='The module name for the scanner class.')
    parser.add_argument('three_module', type=str, nargs='?', default='three.MF.V3.Three', help='The module name for the three functions.')
    parser.add_argument('output_file', type=str, nargs='?', default='./three/scanner.py', help='The output file for the .py content.')
    args = parser.parse_args()
    
    generate_py(args.scanner_module, args.three_module, args.output_file)
    exit(0)