import inspect
import importlib
import ast
import argparse

def get_imports_from_file(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                parts = alias.name.split('.')
                for i in range(1, len(parts) + 1):
                    imports.add('.'.join(parts[:i]))
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            if module:
                parts = module.split('.')
                for i in range(1, len(parts) + 1):
                    imports.add('.'.join(parts[:i]))
    return sorted(imports)

def adjust_signature(signature):
    # Replace NoneType with None in the signature
    return signature.replace('NoneType', 'None')

def generate_pyi(scanner_module_name, three_module_name, output_file):
    print("Generating .pyi file...")
    # Import the modules
    three_module = importlib.import_module(three_module_name)
    scanner_module = importlib.import_module(scanner_module_name)

    # Get the class from scanner.py
    scanner_class = getattr(scanner_module, 'Scanner')

    # Get functions from three.py
    three_functions = inspect.getmembers(three_module, inspect.isfunction)

    # Get import statements from scanner.py and three.py
    scanner_imports = get_imports_from_file(scanner_module.__file__)
    three_imports = get_imports_from_file(three_module.__file__)

    # Combine and deduplicate imports
    all_imports = sorted(set(scanner_imports + three_imports))
    
    # Start generating the .pyi content
    pyi_content = []

    # Add imports
    for imp in all_imports:
        pyi_content.append(f"import {imp}")

    # Add specific imports from typing
    pyi_content.append("from typing import Optional, Callable, Any, Union, List")
    

    # Add class definition
    pyi_content.append("\n\nclass Scanner:")
    
    # Add __init__ method
    init_method = scanner_class.__init__
    init_sig = str(inspect.signature(init_method))
    init_sig = adjust_signature(init_sig)
    pyi_content.append(f"    def __init__{init_sig}: ...")

    # Add other methods from Scanner class
    for name, method in inspect.getmembers(scanner_class, inspect.isfunction):
        if not name.startswith('_'):  # Skip private methods
            sig = str(inspect.signature(method))
            sig = adjust_signature(sig)
            pyi_content.append(f"    def {name}{sig}: ...")

    # Add dynamically bound functions from three.py
    for name, func in three_functions:
        sig = str(inspect.signature(func))
        sig = adjust_signature(sig)
        doc = inspect.getdoc(func)
        pyi_content.append(f"    def {name}{sig}: ...")
        if doc:
            pyi_content.append(f'        """{doc}"""')

    # Write to the output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(pyi_content))
    print("Completed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate .pyi file for a given module.")
    parser.add_argument('scanner_module', type=str, nargs='?', default='three.scanner', help='The module name for the scanner class.')
    parser.add_argument('three_module', type=str, nargs='?', default='three.MF.V3.Three', help='The module name for the three functions.')
    parser.add_argument('output_file', type=str, nargs='?', default='./three/scanner.pyi', help='The output file for the .pyi content.')
    args = parser.parse_args()
    
    generate_pyi(args.scanner_module, args.three_module, args.output_file)
    exit(0)