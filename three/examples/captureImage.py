# Simple Scanner

# Three library
from three.scanner import Scanner
from three.MF.V3.Settings.Camera import Camera
from three.MF.V3.Descriptors.Settings.Camera import Camera as CameraDescriptor
from three.MF.V3.Descriptors.CaptureImage import CaptureImage as CaptureImageDescriptor
from three.MF.V3 import Task

import time

# Camera/Projector settings
camera = Camera(exposure=50000, digitalGain=256, analogGain=256.0)

def main():
   
    # Task update
    def OnTask(task:Task):
        if task.Progress:
            print(f"{int((task.Progress.current/task.Progress.total)*100)} %")
        else:
            print(task.Type,task.Index,task.State)

    # Buffer received
    def OnBuffer(descriptor, buffer:bytes):
    
        # Video task
        if descriptor.Task['Type'] == 'CaptureImage': 
            imageDescriptor = CaptureImageDescriptor(**descriptor.Descriptor)        
            with open(f'camera{imageDescriptor.camera}_image.{imageDescriptor.codec}', 'wb') as f:
                f.write(buffer)
            

    global camera, projector, turntable

    # Connect to the scanner
    scanner = Scanner(OnTask=OnTask, OnBuffer=OnBuffer, OnMessage=None)
    scanner.Connect("ws://matterandform.local:8081")

    # Get the settings stored on the scanner and apply them to the UI
    scanSettingsTask = scanner.list_settings()
    cameraDescriptor = CameraDescriptor(**scanSettingsTask.Output["camera"])

    # camera.exposure = cameraDescriptor.exposure["value"]
    # camera.analogGain = cameraDescriptor.analogGain["value"]
    # camera.digitalGain = cameraDescriptor.digitalGain["value"]
    camera.focus = cameraDescriptor.focus["value"]["default"][0]

    scanner.set_cameras([0], False, 90000, 256, 0, camera.focus)

    scanner.set_projector(False); 
    # Sleep to let the cameras flush the buffer so we don't see the previous projector image
    # Too short and you will get ghosting or a double image
    time.sleep(0.25) 

    # Capture an image
    scanner.capture_image(selection=[0], codec='jpg', grayscale=False)

    scanner.set_projector(True, color=[255, 0, 255])
    time.sleep(0.25)    
    scanner.capture_image(selection=[0], codec='png', grayscale=False)

    scanner.set_projector(True, color=[255, 0, 0])
    time.sleep(0.25)
    scanner.capture_image(selection=[0], codec='raw', grayscale=False)

    scanner.set_projector(True, color=[255, 255, 255])
    time.sleep(0.25)
    scanner.capture_image(selection=[0], codec='bmp', grayscale=True)

    scanner.set_projector(False); 
    scanner.Disconnect()


if __name__ == "__main__":
    main()
