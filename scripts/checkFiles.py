import os
import argparse

from flake8.api import legacy as flake8

def run_flake8(file_path):
    style_guide = flake8.get_style_guide(select=['E', 'F'], ignore=['E501'])
    report = style_guide.check_files([file_path])
    return report.get_statistics('E') + report.get_statistics('F')

def check_files(directory):
    print("Checking python files...")
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
    parser = argparse.ArgumentParser(description="Check python files for formatting and linting issues.")
    parser.add_argument('input_dir', type=str, nargs='?', default='./three/MF/V3/', help='The directory to check for python files.')
    args = parser.parse_args()
    check_files(args.input_dir)