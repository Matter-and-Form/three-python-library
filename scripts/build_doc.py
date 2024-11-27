# Build proto files

import os
import subprocess
import shutil

# Define color variables
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

# Paths
scriptPath = os.path.dirname(os.path.realpath(__file__))
docOutputPath = scriptPath + '/../docs'
module = 'three'

# Remove the docOutputPath if it exists
if os.path.exists(docOutputPath):
    shutil.rmtree(docOutputPath)

# Build the documentation
result = subprocess.run(args=[
    'pdoc',
    '-o',
    docOutputPath,
    module],
    capture_output=True)

if result.returncode == 0:
    print(GREEN + result.stdout.decode('utf-8') + ENDC)
    print(YELLOW + result.stderr.decode('utf-8') + ENDC)
else:
    print('Doc failed')
    print(GREEN + result.stdout.decode('utf-8') + ENDC)
    print(RED + result.stderr.decode('utf-8') + ENDC)