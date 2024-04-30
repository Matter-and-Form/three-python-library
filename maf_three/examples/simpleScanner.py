# Simple Scanner

# OpenCV
import cv2
import numpy as np

# Three library
from maf_three.V3Task import V3Task
from maf_three.scanner import Scanner

from maf_three.settings.capture import Capture
from maf_three.settings.scan import Scan

from maf_three.settings.turntable import Turntable
from maf_three.task import Task, TaskState

from maf_three.settings.camera import Camera
from maf_three.settings.projector import Projector

# Two frames for the video stream
frame0 = np.zeros((0,0,3), np.uint8)
frame1 = np.zeros((0,0,3), np.uint8)

# Camera/Projector settings
camera = Camera(exposure=50000, digitalGain=256, analogGain=256)
projector = Projector(brightness=0.5)
turntable = Turntable(use=False)

def main():

    print('###############################################')
    print('This example required OpenCV for Python')
    print('To install (apt or pip):')
    print('  * sudo apt install python3-opencv')
    print('  * pip install opencv-python')
    print('###############################################')

    ControlsWindow = 'Controls'
    Camera0Window = 'Camera0'
    Camera1Window = 'Camera1'

    # Task update
    def OnTask(task:Task):

        if task.State == TaskState.Completed:
            # New Test Scan
            if(task.Type == V3Task.NewTestScan):
                if task.Output:
                    print('Scan Completed -> Requesting the data')
                    index = task.Output[0]
                    filePath = f'TestScans/Scan-{index}/Scan-{index}.ply'
                    scanner.SendTask(1, V3Task.DownloadFile, filePath )
        
        elif task.State == TaskState.Failed:
            print('Failed Task : ', task)

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
        global camera
        camera.exposure = value
        if scanner.IsConnected(): scanner.SendTask(99, V3Task.SetCameras, Camera(exposure=value))

    def OnTrackbarAnalogGain(value):
        global camera
        camera.analogGain = value
        if scanner.IsConnected(): scanner.SendTask(99, V3Task.SetCameras, Camera(analogGain=value))

    def OnTrackbarDigitalGain(value):
        global camera
        camera.digitalGain = value
        if scanner.IsConnected(): scanner.SendTask(99, V3Task.SetCameras, Camera(digitalGain=value))

    def OnTrackbarProjectorBrightness(value):
        global projector
        projector.brightness = value / 100
        if scanner.IsConnected(): scanner.SendTask(112, V3Task.SetProjector, Projector(brightness=value/100))

    def OnTrackbarUseTurntable(value):
        global turntable
        turntable.use = value == 1

    def OnTrackbarTurntableSweep(value):
        global turntable
        turntable.sweep = value

    def OnTrackbarTurntableSteps(value):
        global turntable
        turntable.steps = value

    try:
        # Connect to the scanner
        scanner = Scanner(OnTask=OnTask, OnBuffer=OnBuffer, OnMessage=None)
        scanner.Connect("ws://matterandform.local:8081")

        # Create the UI
        cv2.namedWindow(ControlsWindow)
        cv2.namedWindow(Camera0Window)
        cv2.namedWindow(Camera1Window)
        cv2.moveWindow(ControlsWindow,0, 550)
        cv2.moveWindow(Camera0Window,0,100)
        cv2.moveWindow(Camera1Window,550,100)
        cv2.createTrackbar('Exposure', ControlsWindow , camera.exposure, 100000, OnTrackbarExposure)
        cv2.createTrackbar('Analog Gain', ControlsWindow , camera.analogGain, 1024, OnTrackbarAnalogGain)
        cv2.createTrackbar('Digital Gain', ControlsWindow , camera.digitalGain, 1024, OnTrackbarDigitalGain)
        cv2.createTrackbar('Projector Brightness', ControlsWindow , int(100 * projector.brightness), 100, OnTrackbarProjectorBrightness)
        cv2.createTrackbar('Use Turntable', ControlsWindow , 1 if turntable.use else 0, 1, OnTrackbarUseTurntable)
        cv2.createTrackbar('Turntable Sweep', ControlsWindow , 180, 360, OnTrackbarTurntableSweep)
        cv2.createTrackbar('Turntable Steps', ControlsWindow , 0, 32, OnTrackbarTurntableSteps)

        # User input loop
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
                
                elif key == 118 : # 'v' => Start video and the projector
                    scanner.SendTask(112, V3Task.SetProjector, Projector(color=[1,1,1], on=True, brightness=projector.brightness))
                    scanner.SendTask(-1, V3Task.StartVideo)       
                
                elif key == 115: # 's' => Create a new Test Scan
                    scan = Scan(
                        camera,
                        Capture(), 
                        projector,
                        turntable)
                    scanner.SendTask(115, V3Task.NewTestScan, scan)
    
    except Exception as error:
        print('Error : ', error)
    except:
        print('An error occurred')
    
    scanner.Disconnect()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
