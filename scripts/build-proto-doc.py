# Build proto files

import os
import subprocess

# Paths
scriptPath = os.path.dirname(os.path.realpath(__file__))
protoInputPath = scriptPath + "/../V3Schema/"
protoOutputPath = scriptPath + "/../doc/source"

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


# Find all the proto files
import glob
files = glob.glob(protoInputPath+"/**/*.proto", recursive=True)

# Build the proto files
result = BuildProtoFiles(files, protoInputPath, protoOutputPath)

# Inspect the results
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'
print("*****************")
if result.returncode == 0:
    print(result.stdout.decode('utf-8'))
    print(GREEN + 'Built : ' + str(len(files)) + ' proto files' + ENDC)
else:
    print('Build failed:')
    print(RED + result.stderr.decode('utf-8') + ENDC)
    exit(1)
print("*****************")

# Build the documentation
result = subprocess.run(args=[
    'sphinx-build',
    '-M',
    'html',
    scriptPath + '/../doc/source/',
    scriptPath + '/../doc/build/'],
    capture_output=True)

print(GREEN + result.stdout.decode('utf-8') + ENDC)
print(RED + result.stderr.decode('utf-8') + ENDC)

