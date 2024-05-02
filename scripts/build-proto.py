# Build proto files

import os
import subprocess

# Paths
scriptPath = os.path.dirname(os.path.realpath(__file__))
protoInputPath = scriptPath + "/../V3Schema"
protoOutputPath = scriptPath + "/../maf_three"

print("*****************")
print("Building Proto files from: " + protoInputPath)
print("Output directory:          " + protoOutputPath)
print("*****************")

def BuildProtoFile(protoFile, inputDir, outputDir):
    print("---> Building: " + file)

    # Build the proto file
    status = subprocess.run([
        'python3',
        '-m',
        'grpc_tools.protoc',
        protoFile,
        f'-I={inputDir}',
        f'--python_out={outputDir}',
        f'--pyi_out={outputDir}',
        '--experimental_allow_proto3_optional'
        ], capture_output=True) 

    return status
    

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

# Find and build all the proto files
fileError = 0
fileCount = 0
import glob
files = glob.glob(protoInputPath+"/**/*.proto", recursive=True)
for file in files:

    # Build
    result = BuildProtoFile(file, protoInputPath, protoOutputPath) 

    # Inspect result
    fileCount += 1
    if result.returncode != 0:
        fileError += 1
        print(RED + result.stderr.decode('utf-8') + ENDC)

# Print results
print("*****************")
print(GREEN + 'Built: ' + str(fileCount - fileError) + " / " + str(fileCount) + " files." + ENDC)
if fileError > 0:   
    print(RED + 'Error: ' +  str(fileError) + " / " + str(fileCount) + " files." + ENDC)
print("*****************")

# Let the caller know if everything was built
exit(0 if fileError == False else 1)
