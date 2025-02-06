from typing import List
import time

# Three library
from three.scanner import Scanner
from three.MF.V3.Settings import Capture, Camera, Projector, Turntable, ScanSelection, Export, Quality
from three.MF.V3.Descriptors import Calibration
from three.MF.V3.Descriptors.Settings import Scanner as ScannerDescriptor, Camera as CameraDescriptor, Projector as ProjectorDescriptor, Turntable as TurntableDescriptor, Capture as CaptureDescriptor

from three.MF.V3 import Task, TaskState


done = False
cornersDetected_0 = 0 # Amount of corners detected on camera 0
cornersDetected_1 = 0 # Amount of corners detected on camera 1
cornersTotal = 0 # Total number of corners to be detected

def main():

    def OnTask(task:Task):
        global done
        # print(json.dumps(task, default=lambda o: o.__dict__, indent=4))
        if task.Progress:
            print(f"{int((task.Progress.current/task.Progress.total)*100)} %")
        else:
            print(task.Type,task.Index,task.State)
            if task.Type == "CalibrateTurntable":
                if task.State == "Completed":
                    print('Calibration Completed')
                elif task.State == "Failed":
                    print('Calibration Failed:', task.Error)
                done = True
            elif task.Type == "DetectCalibrationCard":
                if task.State == "Completed":
                    print('Calibration Card Detection Started')
                elif task.State == "Failed":
                    print('Calibration Card Detection Failed:', task.Error)
                done = True

    def OnBuffer(bufferObject, buffer:bytes):
        global cornersDetected_0, cornersDetected_1, cornersTotal

        # Video task ?
        if bufferObject.Task['Type'] == "Video":
            
            # Calibration card present in the descriptor
            if "calibrationCard" in bufferObject.Descriptor:
                calibrationCard = Calibration.DetectedCard(**bufferObject.Descriptor['calibrationCard'])
                            
                # Total amount of corners
                if cornersTotal == 0:
                    cardWidth = calibrationCard.size[0]
                    cardHeight = calibrationCard.size[1]
                    if cardWidth == 0 or cardHeight == 0:
                        return;
                    cornersTotal = int((cardWidth - 1) * (cardHeight - 1))
                
                if calibrationCard.corners is not None:
                    detectedCorners = calibrationCard.corners
                    detectedCorners = int(len(detectedCorners) / 2)
                    # Camera 0
                    if bufferObject.Index == 0:
                        cornersDetected_0 = detectedCorners
                    # Camera 1
                    else:
                        cornersDetected_1 = detectedCorners
                else:
                    if bufferObject.Index == 0:
                        cornersDetected_0 = 0
                    else:
                        cornersDetected_1 = 0
            
            # No calibration card in the descriptor
            else:
                if bufferObject.Index == 0:
                    cornersDetected_0 = 0
                else:
                    cornersDetected_1 = 0    
            print(f'Camera 0: {cornersDetected_0}/{cornersTotal} ; Camera 1: {cornersDetected_1}/{cornersTotal}')

    try:
        # Connect
        scanner = Scanner(OnTask=OnTask, OnMessage=None, OnBuffer=OnBuffer)
        scanner.Connect("ws://matterandform.local:8081")

        # Start the video
        scanner.start_video()

        # Detect the calibration card
        print('******* Detecting the calibration card')
        scanner.detect_calibration_card(3) # left camera only, 2 = Right camera only, 3 = Both cameras

        # Wait for the calibration card to be detected
        print('Waiting for the calibration card to be detected')
        timeout = time.time() + 10  # 10 seconds from now
        while cornersTotal == 0 and time.time() < timeout:
            time.sleep(0.1)
        if cornersTotal == 0:
            print("Timeout: Calibration card not detected within 10 seconds")

        # Detect the calibration card for 5sec
        time.sleep(5)

        # Stop the video
        scanner.detect_calibration_card(0) # Stop the detection
        scanner.stop_video()

        # Calibration the turntable
        print('\n******* Calibrating the turntable')
        scanner.calibrate_turntable()



    except Exception as error:
        print('Error: ', error)
    except:
        print('Error')

    finally: 
        if scanner.IsConnected():
            scanner.Disconnect()


if __name__ == "__main__":
    main()
