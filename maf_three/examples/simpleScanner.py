# Simple Scanner

import numpy as np

# Three library
from maf_three.scanner import Scanner
from maf_three.MF.V3.Settings import Camera, Projector, Turntable, Scan, Capture
from maf_three.MF.V3.Descriptors import Project
from maf_three.MF.V3.Descriptors.Settings import Scanner as ScannerDescriptor, Camera as CameraDescriptor, Projector as ProjectorDescriptor, Turntable as TurntableDescriptor
from maf_three.MF.V3 import Task, TaskState
# Two frames for the video stream
frame0 = np.zeros((0,0,3), np.uint8)
frame1 = np.zeros((0,0,3), np.uint8)

# Camera/Projector settings
camera = Camera(exposure=50000, digitalGain=256, analogGain=256.0)
projector = Projector(on=True, brightness=0.5)
turntable = Turntable(8,360,False)

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

        if task.Progress:
            print(task.Progress)
        else:
            print(task.State)
        # if task.State == TaskState.Completed:
            # New Test Scan
            # if(task.Type == V3Task.NewTestScan):
            #     if task.Output:
            #         print('Scan Completed -> Requesting the data')
            #         index = task.Output[0]
            #         filePath = f'TestScans/Scan-{index}/Scan-{index}.ply'
            #         scanner.SendTask(1, V3Task.DownloadFile, filePath )
        
        # elif task.State == TaskState.Failed:
        #     print('Failed Task: ', task)

    # Buffer received
    def OnBuffer(descriptor, buffer:bytes):
        global frame0, frame1
    
        # Video task
        if descriptor['Task']['Index'] == -1:
            if descriptor['Index'] == 0:
                frame0 = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_COLOR)
            else:
                frame1 = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_COLOR)
        
        # DownloadFile
        elif descriptor['Task']['Index'] == 1:
            with open('scan.ply', 'wb') as binary_file:
                binary_file.write(buffer)
            print('Scan saved into scan.ply')


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
        turntable.steps = value

    def OnTrackbarFocus(value):
        camera.focus = value
        scanner.set_cameras(focus=value)


    try:
        global camera, projector, turntable

        # Connect to the scanner
        scanner = Scanner(OnTask=OnTask, OnBuffer=OnBuffer, OnMessage=None)
        scanner.Connect("ws://matterandform.local:8081")

        scanSettingsTask = scanner.list_settings()
        cameraDescriptor = CameraDescriptor(**scanSettingsTask.Output["camera"])
        projectorDescriptor = ProjectorDescriptor(**scanSettingsTask.Output["projector"])
        turntableDescriptor = TurntableDescriptor(**scanSettingsTask.Output["turntable"])

        camera.exposure = cameraDescriptor.exposure["value"]
        camera.analogGain = cameraDescriptor.analogGain["value"]
        camera.digitalGain = cameraDescriptor.digitalGain["value"]
        camera.focus = cameraDescriptor.focus["value"]["default"][0]
        projector.brightness = projectorDescriptor.brightness["value"]
        turntable.use = False
        turntable.sweep = turntableDescriptor.sweep["value"]
        turntable.scans = turntableDescriptor.scans["value"]

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
                    if turntable.use:
                        scanner.new_scan(camera=camera, projector=projector, turntable=turntable)
                    else:
                        scanner.new_scan(camera=camera, projector=projector)
    
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
