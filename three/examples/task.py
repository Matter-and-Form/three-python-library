import json
from typing import List

# Three library
from three.scanner import Scanner
from three.MF.V3.Settings import Capture, Camera, Projector
from three.MF.V3.Descriptors import Project
from three.MF.V3 import Task, TaskState


done = False

def main():
    global done

    # Task update
    def OnTask(task:Task):
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
        scanner.new_scan()

        projectTask = scanner.list_projects()
        if projectTask.Error:
            print('Error:', projectTask.Error)
            return
        
        for project_obj in projectTask.Output:
            project = Project.Brief(**project_obj)
            print('Project index:', project.index, ' - Name:', project.name)

    except Exception as error:
        print('Error: ', error)
    except:
        print('Error')

    finally: 
        if scanner.IsConnected():
            scanner.Disconnect()

if __name__ == "__main__":
    main()
