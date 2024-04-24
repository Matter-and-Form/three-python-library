# Task
import time

from maf_three.scanner import Scanner
from maf_three.settings.camera import Camera
from maf_three.settings.capture import Capture
from maf_three.settings.projector import Projector
from maf_three.settings.scan import Scan
from maf_three.task import Task, TaskState
from maf_three.V3Task import V3Task

done = False

def OnTask(task:Task):
    global done

    # Inspect Task State
    match task.State:

        # Started
        case TaskState.Started:
            print('\nTask Started:\tIndex:', task.Index, ' - ' ,task.Type)

        # Completed
        case TaskState.Completed:
            print('Task Completed:\tIndex:', task.Index, ' - ' , task.Type)
            if(task.Index == 1):
                done = True
        
        # Failed
        case TaskState.Failed:
            print('Task Failed:\tIndex:', task.Index, ' - ', task.Type, ' - Error:', task.Error)
            if(task.Index == 1):
                done = True

    # Track Task Progress
    if task.Progress != None:
        progress = task.Progress['ScanProcess']
        print(progress['current'] , '/', progress['total'], '-', progress['step'])


try:
    # Connect
    scanner = Scanner(OnTask=OnTask, OnMessage=None, OnBuffer=None)
    scanner.Connect("ws://matterandform.local:8081")

    # Try to scan without input => Will trigger an error
    scanner.SendTask(0, V3Task.NewTestScan)

    # Scan
    scan = Scan(
        Camera(analogGain=256,digitalGain=256,exposure=50000),
        Capture(), 
        Projector(brightness=0.5)
    )
    scanner.SendTask(1, V3Task.NewTestScan, scan)

    # Wait for the tasks to finish
    while not done:
        time.sleep(0.1)


except Exception as error:
    print('Error : ', error)
except:
    print('Error')

finally: 
    if scanner.IsConnected():
        scanner.Disconnect()