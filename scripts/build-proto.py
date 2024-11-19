import subprocess
import os
import inspect
import importlib
import ast

import transpileProto
from flake8.api import legacy as flake8
import shutil
    

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
    # Import the modules
    scanner_module = importlib.import_module(scanner_module_name)
    three_module = importlib.import_module(three_module_name)

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
        pyi_content.append(f"    def {name}{sig}: ...")

    # Write to the output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(pyi_content))


def run_flake8(file_path):
    style_guide = flake8.get_style_guide(select=['E', 'F'], ignore=['E501'])
    report = style_guide.check_files([file_path])
    return report.get_statistics('E') + report.get_statistics('F')

def check_files(directory):
    hasError = False
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                filepath = os.path.join(root, file)
                # print(f"Running flake8 on {filepath}...")
                flake8_output = run_flake8(filepath)
                if flake8_output:
                    print(f"flake8 issues in {filepath}:\n{flake8_output}")
                    hasError = True
                else:
                    print(f"Clean: {filepath}")
    if hasError:
        raise Exception("Formatting Or Linting Issues Found")

if __name__ == "__main__":
    # Remove the folder maf_three/MF if it exists
    mf_folder = "./maf_three/MF"
    if os.path.exists(mf_folder):
        shutil.rmtree(mf_folder)
    print("Building python files...")
    transpileProto.transpile("./V3Schema/", "./maf_three/")
    print("Checking python files...")
    check_files("./maf_three/MF/V3/")
    print("Generating .pyi file...")
    generate_pyi('maf_three.scanner', 'maf_three.MF.V3.Three', './maf_three/scanner.pyi')
    print("Completed!")
    exit(0)