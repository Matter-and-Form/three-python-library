# 01_simpleScanner.py

# OpenCV
import cv2
import numpy as np

# Three API
from three_api.V3Task import V3Task
from three_api.scanner import Scanner

from three_api.settings.capture import Capture
from three_api.settings.scan import Scan

from three_api.task import Task, TaskState

from three_api.settings.camera import Camera
from three_api.settings.projector import Projector

ControlsWindow = 'Controls'
Camera0Window = 'Camera0'
Camera1Window = 'Camera1'

# Two frames for the video stream
frame0 = np.zeros((0,0,3), np.uint8)
frame1 = np.zeros((0,0,3), np.uint8)

# Camera/Projector settings
exposure = 50000
digitalGain = 256
analogGain = 256
projectorBrightness = 0.5

# Message received
def OnMessage(incoming:str):
    print('Message : ', incoming)

# Task update
def OnTask(incoming:Task):

    if incoming.State == TaskState.Completed:
        # New Test Scan
        if(incoming.Type == V3Task.NewTestScan):
            if incoming.Output:
                print('Scan Completed -> Requesting the data')
                index = incoming.Output[0]
                filePath = f'TestScans/Scan-{index}/Scan-{index}.ply'
                scanner.SendTask(1, V3Task.DownloadFile, filePath )
    
    elif incoming.State == TaskState.Failed:
       print('Failed Task : ', incoming)

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
    global exposure
    exposure = value
    if scanner.IsConnected(): scanner.SendTask(99, V3Task.SetCameras, Camera(exposure=exposure))

def OnTrackbarAnalogGain(value):
    global analogGain
    analogGain = value
    if scanner.IsConnected(): scanner.SendTask(99, V3Task.SetCameras, Camera(analogGain=analogGain))

def OnTrackbarDigitalGain(value):
    global digitalGain
    digitalGain = value
    if scanner.IsConnected(): scanner.SendTask(99, V3Task.SetCameras, Camera(digitalGain=digitalGain))

def OnTrackbarProjectorBrightness(value):
    global projectorBrightness
    projectorBrightness = value / 100
    if scanner.IsConnected(): scanner.SendTask(112, V3Task.SetProjector, Projector(brightness=projectorBrightness))


if __name__ == "__main__":

    try:
        # Connect to the scanner
        scanner = Scanner(OnTask=OnTask, OnMessage=OnMessage, OnBuffer=OnBuffer)
        scanner.Connect("ws://matterandform.local:8081")

        # Create the UI
        cv2.namedWindow(ControlsWindow)
        cv2.namedWindow(Camera0Window)
        cv2.namedWindow(Camera1Window)
        cv2.moveWindow(ControlsWindow,0, 550)
        cv2.moveWindow(Camera0Window,0,100)
        cv2.moveWindow(Camera1Window,550,100)
        cv2.createTrackbar('Exposure', ControlsWindow , exposure, 100000, OnTrackbarExposure)
        cv2.createTrackbar('Analog Gain', ControlsWindow , analogGain, 1024, OnTrackbarAnalogGain)
        cv2.createTrackbar('Digital Gain', ControlsWindow , digitalGain, 1024, OnTrackbarDigitalGain)
        cv2.createTrackbar('Projector Brightness', ControlsWindow , int(100 * projectorBrightness), 100, OnTrackbarProjectorBrightness)

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
                
                elif key == 118 : # Start video and the projector
                    scanner.SendTask(112, V3Task.SetProjector, Projector(color=[1,1,1], on=True, brightness=projectorBrightness))
                    scanner.SendTask(-1, V3Task.StartVideo)       
                
                elif key == 115: # Create a new Test Scan
                    scan = Scan(
                        Camera(analogGain=analogGain,digitalGain=digitalGain,exposure=exposure),
                        Capture(), 
                        Projector(brightness=projectorBrightness))
                    scanner.SendTask(115, V3Task.NewTestScan, scan)

    except:
        print('An error occurred')
    

    scanner.Disconnect()
    cv2.destroyAllWindows()
