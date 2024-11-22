# Simple Scanner

import numpy as np
import json
from typing import List

# Three library
from three.scanner import Scanner
from three.MF.V3.Settings.Projector import Projector
from three.MF.V3.Settings.Capture import Capture
from three.MF.V3.Settings.Camera import Camera
from three.MF.V3.Settings.Turntable import Turntable
from three.MF.V3.Settings.ScanSelection import ScanSelection
from three.MF.V3.Settings.Export import Export
from three.MF.V3.Settings.Quality import Quality
from three.MF.V3.Descriptors.Project import Project
from three.MF.V3.Descriptors.Settings.Camera import Camera as CameraDescriptor
from three.MF.V3.Descriptors.Settings.Projector import Projector as ProjectorDescriptor
from three.MF.V3.Descriptors.Settings.Turntable import Turntable as TurntableDescriptor
from three.MF.V3.Descriptors.Settings.Capture import Capture as CaptureDescriptor

from three.MF.V3 import Task, TaskState
# Two frames for the video stream
frame0 = np.zeros((0,0,3), np.uint8)
frame1 = np.zeros((0,0,3), np.uint8)


# Camera/Projector settings
camera = Camera(exposure=50000, digitalGain=256, analogGain=256.0)
projector = Projector(on=True, brightness=0.5)
turntable = Turntable(8,360,False)
capture = Capture(Quality.Low,False)

scanTaskIndex = -1

def main():

    # OpenCV
    try:
        import cv2

    except ModuleNotFoundError as error:
        print('###############################################')
        print('This example required OpenCV for Python')
        print('To install (apt or pip):')
        print('  * sudo apt install python3-opencv')
        print('  * pip3 install opencv-python')
        print('###############################################')
        exit(1)

    ControlsWindow = 'Controls'
    Camera0Window = 'Camera0'
    Camera1Window = 'Camera1'

    # Task update
    def OnTask(task:Task):
        # print(json.dumps(task, default=lambda o: o.__dict__, indent=4))
        if task.Progress:
            print(f"{int((task.Progress.current/task.Progress.total)*100)} %")
        else:
            print(task.Type,task.Index,task.State)

    # Buffer received
    def OnBuffer(descriptor, buffer:bytes):
        global frame0, frame1
    
        # Video task
        if descriptor.Task['Type'] == 'Video': 
            if descriptor.Index == 0:
                frame0 = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_COLOR)
            else:
                frame1 = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_COLOR)
        
        # DownloadFile
        elif descriptor.Task['Type'] == "Export":
            with open('scan.zip', 'wb') as binary_file:
                binary_file.write(buffer)
            print('Scan saved into scan.zip')


    def OnTrackbarExposure(value):
        # Exposure Min in 9000
        if (value < 9000):
            value = 9000
        camera.exposure = value
        scanner.set_cameras(exposure=value)

    def OnTrackbarAnalogGain(value):
        camera.analogGain = value
        scanner.set_cameras(analogGain=value)
        
    def OnTrackbarDigitalGain(value):
        camera.digitalGain = value
        scanner.set_cameras(digitalGain=value)

    def OnTrackbarProjectorBrightness(value):
        projector.brightness = value/100
        scanner.set_projector(brightness=value/100)

    def OnTrackbarUseTurntable(value):
        global turntable
        turntable.use = value == 1

    def OnTrackbarTurntableSweep(value):
        global turntable
        turntable.sweep = value

    def OnTrackbarTurntableSteps(value):
        global turntable
        turntable.scans = value

    def OnTrackbarFocus(value):
        camera.focus = value
        scanner.set_cameras(focus=value)

    def OnTrackbarQuality(value):
        global capture
        capture.quality = getQualityFromInt(value)

    def OnTrackbarTexture(value):
        global capture
        capture.texture = value == 1

    def getIntFromQuality(quality:Quality) -> int:
        if quality == Quality.Low.value:
            return 0
        elif quality == Quality.Medium.value:
            return 1
        elif quality == Quality.High.value:
            return 2
    
    def getQualityFromInt(quality:int) -> Quality:
        if quality == 0:
            return Quality.Low
        elif quality == 1:
            return Quality.Medium
        elif quality == 2:
            return Quality.High

    try:
        global camera, projector, turntable

        # Connect to the scanner
        scanner = Scanner(OnTask=OnTask, OnBuffer=OnBuffer, OnMessage=None)
        scanner.Connect("ws://matterandform.local:8081")

        # Get the settings stored on the scanner and apply them to the UI
        scanSettingsTask = scanner.list_settings()
        cameraDescriptor = CameraDescriptor(**scanSettingsTask.Output["camera"])
        projectorDescriptor = ProjectorDescriptor(**scanSettingsTask.Output["projector"])
        turntableDescriptor = TurntableDescriptor(**scanSettingsTask.Output["turntable"])
        captureDescriptor = CaptureDescriptor(**scanSettingsTask.Output["capture"])

        camera.exposure = cameraDescriptor.exposure["value"]
        camera.analogGain = cameraDescriptor.analogGain["value"]
        camera.digitalGain = cameraDescriptor.digitalGain["value"]
        camera.focus = cameraDescriptor.focus["value"]["default"][0]
        projector.brightness = projectorDescriptor.brightness["value"]
        turntable.use = False
        turntable.sweep = turntableDescriptor.sweep["value"]
        turntable.scans = turntableDescriptor.scans["value"]
        capture.quality = captureDescriptor.quality["value"]
        capture.texture = captureDescriptor.texture["value"]

        # Create the UI
        cv2.namedWindow(ControlsWindow)
        cv2.namedWindow(Camera0Window)
        cv2.namedWindow(Camera1Window)
        cv2.moveWindow(ControlsWindow,0, 550)
        cv2.moveWindow(Camera0Window,0,100)
        cv2.moveWindow(Camera1Window,550,100)
        cv2.createTrackbar('Exposure', ControlsWindow, int(camera.exposure), int(cameraDescriptor.exposure["max"]), OnTrackbarExposure)
        cv2.createTrackbar('Camera Focus', ControlsWindow, int(camera.focus), int(cameraDescriptor.focus["value"]["max"]), OnTrackbarFocus)
        cv2.createTrackbar('Analog Gain', ControlsWindow, int(camera.analogGain), int(cameraDescriptor.analogGain["max"]), OnTrackbarAnalogGain)
        cv2.createTrackbar('Digital Gain', ControlsWindow, int(camera.digitalGain), int(cameraDescriptor.digitalGain["max"]), OnTrackbarDigitalGain)
        cv2.createTrackbar('Projector Brightness', ControlsWindow, int(100 * projector.brightness), 100, OnTrackbarProjectorBrightness)
        cv2.createTrackbar('Use Turntable', ControlsWindow, 1 if turntable.use else 0, 1, OnTrackbarUseTurntable)
        cv2.createTrackbar('Turntable Sweep', ControlsWindow, int(turntable.sweep), int(turntableDescriptor.sweep["max"]), OnTrackbarTurntableSweep)
        cv2.createTrackbar('Turntable Scans', ControlsWindow, int(turntable.scans), int(turntableDescriptor.scans["max"]), OnTrackbarTurntableSteps)
        cv2.createTrackbar('Capture Quality', ControlsWindow, getIntFromQuality(capture.quality), 2, OnTrackbarQuality)
        cv2.createTrackbar('Capture Texture', ControlsWindow, 1 if capture.texture else 0, 1, OnTrackbarTexture)

        new_project_return = scanner.new_project('SimpleScanner')
        project:Project = Project(**new_project_return.Output)
        scanner.open_project(project.index)
    
        # Turn on the projector and start the video
        scanner.set_projector(on=True, brightness=projector.brightness, color=[1,1,1])
        scanner.start_video()
        

        # User input loop
        print('Press "Esc" to quit.')  
        while True:

            # If present => Show the frames
            if frame0.size > 0:
                cv2.imshow(Camera0Window,frame0)
            if frame1.size > 0:
                cv2.imshow(Camera1Window,frame1)
            # User input
            key = cv2.waitKey(1)
            if(key != -1):

                if key == 27: # Esc => Break the loop
                    break
                
                elif key == 115: # 's' => Create a new Test Scan
                    scanner.new_scan(camera=camera, projector=projector, turntable=turntable if turntable.use else None, capture=capture)
                    scanner.export(selection=ScanSelection(ScanSelection.Mode.all) ,merge=True, texture=True, format=Export.Format.ply)
                    
                elif key == 108: # 'l' => List all scans in the current project
                    list_project_return = scanner.list_projects()
                    project_list: List[Project.Brief] = []
                    for proj in list_project_return.Output:
                        project_list.append(Project.Brief(**proj))
                    for proj in project_list:
                        print(f"Project Index: {proj.index}, Project Name: {proj.name}")
    
    except Exception as error:
        print('Error: ', error)
    
    finally:
        if scanner.IsConnected():
            if project:
                scanner.remove_projects([project.index])
            scanner.set_projector(on=False)

    
    scanner.Disconnect()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
