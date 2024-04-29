# examples entry point

import sys

from maf_three.examples import  connection, projector, turntable, task, simpleScanner


# Examples dictionary 
examples = {
    'connection': connection.main,
    'projector': projector.main,
    'turntable': turntable.main,
    'task': task.main,
    'simpleScanner': simpleScanner.main
}

def PrintExampleList():
    print('Available examples')
    for ex in examples:
        print('  *',ex)

# Argument provided ?
if len(sys.argv) == 1:
    print("Please enter an example name")
    PrintExampleList()
    exit(1)

# Get the example from the argument
arg = sys.argv[1]

# Example exists ?
if arg not in examples:
    print('Unknown example : ', arg)
    PrintExampleList()
    exit(1)

# Run
print("Running example : " , arg)
examples[arg]()






