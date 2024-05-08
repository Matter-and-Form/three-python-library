# Build proto files

import os
import subprocess
import glob
import re

# Paths
scriptPath = os.path.dirname(os.path.realpath(__file__))
protoInputPath = scriptPath + "/../V3Schema/"
protoOutputPath = scriptPath + "/../maf_three"

print("*****************")
print("Building Proto files from: " + protoInputPath)
print("Output directory:          " + protoOutputPath)
print("*****************")


def BuildProtoFiles(protoFiles, inputDir, outputDir):
    for file in protoFiles:
        print("---> Building: " + file)

    status = subprocess.run(args=[
        'python3',
        '-m',
        'grpc_tools.protoc',
        f'-I={inputDir}',
        f'--python_betterproto_out={outputDir}',
        '--experimental_allow_proto3_optional']
        + protoFiles,
        capture_output=True) 

    return status

def CleanUpGeneratedInit(file):

    # Get the content
    with open(file, "r") as f:
        lines = f.readlines()

    # Filter output
    with open(file, "w") as f:
        badImport = False
        for line in lines:

            # Beginning of the imports ?
            if 'from ....' in line:
                badImport = True

            # Outside of the import section ?
            if not badImport:
                if 'MfV3' in line:
                    line = re.sub('"[_]{3,}MfV3Settings', '"MF.V3.Settings.', line)
                    line = re.sub('"[_]{3,}MfV3Descriptors', '"MF.V3.Descriptors.', line)
                    line = line.replace('__"', '"')

                f.write(line)

            # End of the imports
            if badImport and ')' in line:
                badImport = False


# Find all the proto files
protoFiles = glob.glob(protoInputPath+"/**/*.proto", recursive=True)

# Build the proto files
result = BuildProtoFiles(protoFiles, protoInputPath, protoOutputPath)

# Inspect the results
GREEN = '\033[92m'
YELLOW = '\033[33m'
RED = '\033[91m'
ENDC = '\033[0m'
print("*****************")
if result.returncode == 0:
    print(result.stdout.decode('utf-8'))
    print(GREEN + 'Built : ' + str(len(protoFiles)) + ' proto files' + ENDC)
else:
    print('Build failed:')
    print(RED + result.stderr.decode('utf-8') + ENDC)
    exit(result.returncode)
print("*****************")


# Clean up the generated code
generatedFiles = glob.glob(protoOutputPath+"/MF/**/__init__.py", recursive=True)
for file in generatedFiles:
    print('Clean up: ', file)
    CleanUpGeneratedInit(file)


# Build the documentation
result = subprocess.run(args=[
    'sphinx-build',
    '-M',
    'html',
    scriptPath + '/../doc/source/',
    scriptPath + '/../doc/build/',
    '--write-all'],
    capture_output=True)

if result.returncode == 0:
    print(GREEN + result.stdout.decode('utf-8') + ENDC)
    print(YELLOW + result.stderr.decode('utf-8') + ENDC)
else:
    print('Doc failed')
    print(GREEN + result.stdout.decode('utf-8') + ENDC)
    print(RED + result.stderr.decode('utf-8') + ENDC)
    exit(result.returncode)


# Remove generated files
for file in generatedFiles:
    print('Remove:', file)
    os.remove(file)


