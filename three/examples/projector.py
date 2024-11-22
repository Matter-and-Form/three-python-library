# Projector

import sys
import os
import time
import numpy as np

# from three.scanner import Scanner
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from three.scanner import Scanner
import three.MF.V3.Three as Three
from three.MF.V3.Settings.Projector import Projector
from three.MF.V3.Settings.Video import Video
from three.MF.V3.Settings.Rectangle import Rectangle

def main():

    try:
        scanner = Scanner(OnTask=None, OnMessage=None, OnBuffer=None)
        scanner.Connect("ws://matterandform.local:8081")
        
        # Set white color
        scanner.set_projector(color=[1,1,1], on=True, brightness=1.0)
        # Sleep for 1 second
        time.sleep(1)

        # Set red color
        scanner.set_projector(color=[1,0,0])
        # Sleep for 1 second
        time.sleep(1)

        # Set green color
        scanner.set_projector(color=[0,1,0])
        # Sleep for 1 second
        time.sleep(1)

        # Set blue color
        scanner.set_projector(color=[0,0,1])
        # Sleep for 1 second
        time.sleep(1)
        
        # Set brightness to 0.25. The other settings will persist
        scanner.set_projector(brightness=0.25)
        time.sleep(1)
        
        pattern = Projector.Pattern(Projector.Orientation.Vertical,4, 1)
        scanner.set_projector(True, 1.0, pattern, None)
        time.sleep(1)

        ### Project an image
        print('Project Image')
        width = 856
        height = 480
        img = np.zeros([height, width, 3], np.uint8)
        for y in range(height):
            for x in range(0, width):
                img[y,x] = (
                    255 * y / height , # Blue
                    255 * x / width , # Green
                    255 - 255 * y / height # Red
                )
        source = Projector.Image.Source(format = Video.Format.BGR888, width=width, height=height, step=3*width, fixAspectRatio=True)
        scanner.set_projector(on=True, image=Projector.Image(source, Rectangle(0,0,width,height)), color=None, buffer=img.tobytes())
        
        time.sleep(1)

        #### Turn OFF
        scanner.set_projector(on=False)

    except Exception as error:
        print('Error: ', error)
    except:
        print('Error')

    finally: 
        if scanner.IsConnected():
            scanner.Disconnect()
        print('Finally')

if __name__ == "__main__":
    main()
