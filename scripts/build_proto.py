import subprocess
import os
import sys
import shutil

from transpileProto import transpile
from checkFiles import check_files

if __name__ == "__main__":
    # Remove the folder maf_three/MF if it exists
    mf_folder = "./maf_three/MF"
    if os.path.exists(mf_folder):
        shutil.rmtree(mf_folder)
    
    # Transpile the proto files
    transpile('./V3Schema','./maf_three/')

    # Check the python files for formatting and linting issues
    check_files('./maf_three/MF/V3/')

     # These have to be done in subprocesses because the imports are not available in the current process. Chicken and egg problem
    # Add the scripts folder to the system path
    scripts_folder = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, scripts_folder)
    
    # Install the package in editable mode 
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-e', '.'])

    # Generate the proto files
    subprocess.check_call([sys.executable, f'{scripts_folder}/generatePyi.py'])
    
    exit(0)