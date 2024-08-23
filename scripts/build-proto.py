# Build proto files

import os
import subprocess
import glob


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

# Delete previously compiled directory
previousProtoOutputPath = protoOutputPath + "/MF"

if os.path.exists(previousProtoOutputPath):
    print("Deleting previously compiled directory: " + previousProtoOutputPath)
    os.system("rm -rf " + previousProtoOutputPath)

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
if fileError > 0:
    exit(1)

# Remove the _pb2 at the end of the generated files
generatedFiles = glob.glob(protoOutputPath+"/MF/**/*_pb2.*", recursive=True)
for file in generatedFiles:
    print('Updating generated file:', file)    

    # Get the content
    with open(file, "r") as f:
        lines = f.readlines()

    # Remove '_pb2'
    with open(file, "w") as f:
        for line in lines:
            line = line.replace('_pb2', '')
            f.write(line)
    
    # Rename the file
    os.rename(file, file.replace('_pb2', ''))
