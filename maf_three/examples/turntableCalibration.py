# Turntable calibration

import time

from maf_three.scanner import Scanner
from maf_three.task import Task, TaskState
from maf_three.V3Task import V3Task


done = False
cornersDetected_0 = 0 # Amount of corners detected on camera 0
cornersDetected_1 = 0 # Amount of corners detected on camera 1
cornersTotal = 0 # Total number of corners to be detected

def main():

    def OnTask(task:Task):
        global done

        # Calibrate turntable task
        if task.Type == V3Task.CalibrateTurntable:
            # Task progress
            if task.Progress != None:
                progress = task.Progress['CalibrateTurntable']
                print(progress['current'] , '/', progress['total'], '-', progress['step'])

            # Task completed ?
            if task.State == TaskState.Completed:
                print('Calibration Completed')
                print(task.Output)
                done = True
            # Task failed ?
            elif task.State == TaskState.Failed:
                print('Calibration Failed')
                print('Calibration error:', task.Error)
                done = True

    def OnBuffer(descriptor, buffer:bytes):
        global cornersDetected_0, cornersDetected_1, cornersTotal

        # Video task ?
        if descriptor['Task']['Index'] == -1:
            # Calibration card present in the descriptor
            if "calibrationCard" in descriptor['Descriptor']:
                calibrationCard = descriptor['Descriptor']['calibrationCard']
                         
                # Total amount of corners
                if cornersTotal == 0:
                    cardWidth = calibrationCard['size'][0]
                    cardHeight = calibrationCard['size'][1]
                    cornersTotal = (cardWidth - 1) * (cardHeight - 1)

                
                detectedCorners = len(calibrationCard['corners'])
                # Camera 0
                if descriptor['Index'] == 0:
                    cornersDetected_0 = detectedCorners
                # Camera 1
                else:
                    cornersDetected_1 = detectedCorners              
            
            # No calibration card in the descriptor
            else:
                if descriptor['Index'] == 0:
                    cornersDetected_0 = 0
                else:
                    cornersDetected_1 = 0    

            print(f'Camera 0: {cornersDetected_0}/{cornersTotal} ; Camera 1: {cornersDetected_1}/{cornersTotal}     ', end="\r", flush=True)

    try:
        # Connect
        scanner = Scanner(OnTask=OnTask, OnMessage=None, OnBuffer=OnBuffer)
        scanner.Connect("ws://matterandform.local:8081")

        # Start the video
        scanner.SendTask(-1, V3Task.StartVideo)   

        # Detect the calibration card
        print('******* Detecting the calibration card')
        scanner.SendTask(0, V3Task.DetectCalibrationCard, 3)

        # Wait for the calibration card to be detected
        while cornersTotal == 0:
            time.sleep(0.1)

        # Detect the calibration card for 5sec
        time.sleep(5)

        # Stop the video
        scanner.SendTask(-1, V3Task.StopVideo)
        time.sleep(1)

        # Calibration the turntable
        print('\n******* Calibrating the turntable')
        scanner.SendTask(1, V3Task.CalibrateTurntable)

        # Wait for the tasks to finish
        while not done:
            time.sleep(0.1)


    except Exception as error:
        print('Error: ', error)
    except:
        print('Error')

    finally: 
        if scanner.IsConnected():
            scanner.Disconnect()


if __name__ == "__main__":
    main()
