# examples entry point

import sys

from maf_three.examples import  connection, projector, turntable, task#, simpleScanner

# Available examples dictionary 
examples = {
    'connection': connection.main,
    'projector': projector.main,
    'turntable': turntable.main,
    'task': task.main,
    #'simpleScanner': simpleScanner.main
}


def PrintExampleList():
    print('Available examples:')
    for ex in examples:
        print('  *',ex)
    print('Run via:')
    print('python3 -m maf_three.examples {example_name}')

# No argument provided ?
if len(sys.argv) == 1:
    print("Please enter an example name")
    PrintExampleList()
    exit(1)

# Get the example from the argument
arg = sys.argv[1]

if arg.lower() == 'list':
    PrintExampleList()
    exit(0)

# Example exists ?
if arg not in examples:
    print('Unknown example : ', arg)
    PrintExampleList()
    exit(1)

# Run
print("Running example : " , arg)
examples[arg]()






