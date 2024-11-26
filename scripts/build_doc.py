# Build proto files

import os
import subprocess
# Define color variables
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

# Paths
scriptPath = os.path.dirname(os.path.realpath(__file__))
docInputPath = scriptPath + '/../doc/source/'
docOutputPath = scriptPath + '/../doc/build/'

# Build the documentation
result = subprocess.run(args=[
    'sphinx-build',
    '-M',
    'html',
    docInputPath,
    docOutputPath,
    '--write-all'],
    capture_output=True)

if result.returncode == 0:
    print(GREEN + result.stdout.decode('utf-8') + ENDC)
    print(YELLOW + result.stderr.decode('utf-8') + ENDC)
else:
    print('Doc failed')
    print(GREEN + result.stdout.decode('utf-8') + ENDC)
    print(RED + result.stderr.decode('utf-8') + ENDC)

