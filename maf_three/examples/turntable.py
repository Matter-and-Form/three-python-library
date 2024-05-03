# Turntable

from maf_three.scanner import Scanner
from maf_three.task import Task, TaskState
from maf_three.V3Task import V3Task

import time

hasTurntable = None
rotating = False

def main():
    global hasTurntable, rotating

    def OnTask(task:Task):
        global hasTurntable, rotating

        # HasTurntable
        if task.Type == V3Task.HasTurntable and task.State == TaskState.Completed:
            print('Completed : ', task.Output)
            hasTurntable = task.Output

        # RotateTurntable
        elif task.Type == V3Task.RotateTurntable:
            if task.State == TaskState.Started:
                rotating = True
            elif task.State == TaskState.Completed:
                rotating = False

    try:
        scanner = Scanner(OnTask=OnTask, OnMessage=None, OnBuffer=None)
        scanner.Connect("ws://matterandform.local:8081")

        # Check if a Turntable is connected to the scanner
        scanner.SendTask(0, V3Task.HasTurntable)
        while hasTurntable == None:
            #print(hasTurntable)
            pass
        if hasTurntable == False:
            raise Exception('There is no turntable connected to the scanner')

        while True:

            while rotating:
                time.sleep(0.1)

            userInput = input('Enter an angle or "q" to quit\n')

            if userInput.lower() == 'q':
                break

            try:
                angle = float(userInput)
                rotating = True
                scanner.SendTask(0, V3Task.RotateTurntable, angle)
            except:
                pass


    except Exception as error:
        print('Error: ', error)
    except:
        print('Error')

    finally: 
        if scanner.IsConnected():
            scanner.Disconnect()

if __name__ == "__main__":
    main()