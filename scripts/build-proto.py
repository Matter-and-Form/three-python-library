import subprocess
import os

# Build proto files

def run_transpile_proto():
    script_path = os.path.join(os.path.dirname(__file__), 'transpileProto.py')
    input_dir = './V3Schema'
    output_dir = './maf_three/'
    result = subprocess.run(['python', script_path, input_dir, output_dir], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Output: {result.stdout}")

if __name__ == "__main__":
    run_transpile_proto()