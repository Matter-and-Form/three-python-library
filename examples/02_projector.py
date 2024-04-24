# Projector

from three_api.buffer import Buffer
from three_api.scanner import Scanner
from three_api.settings.projector import Image, Orientation, Pattern, Projector, Rect, Source
from three_api.settings.video import Format
from three_api.V3Task import V3Task

import time
import numpy as np

hasTurntable = None
rotating = False

try:
    scanner = Scanner(OnTask=None, OnMessage=None, OnBuffer=None)
    scanner.Connect("ws://matterandform.local:8081")

    #### Turn ON
    scanner.SendTask(0, V3Task.SetProjector, Projector(on=True, brightness=1.0, color=[1,1,1]))
    time.sleep(1)

    #### Project Red
    scanner.SendTask(1, V3Task.SetProjector, Projector(color=[1,0,0]))
    time.sleep(1)

    #### Project Green
    scanner.SendTask(2, V3Task.SetProjector, Projector(color=[0,1,0]))
    time.sleep(1)

    #### Project Blue
    scanner.SendTask(3, V3Task.SetProjector, Projector(color=[0,0,1]))
    time.sleep(1)

    #### Project Vertical Pattern
    scanner.SendTask(4, V3Task.SetProjector, Projector(pattern=Pattern(Orientation.Vertical,frequency=4,phase=1)))
    time.sleep(1)

    #### Project Horizontal Pattern
    scanner.SendTask(5, V3Task.SetProjector, Projector(pattern=Pattern(Orientation.Horizontal,frequency=4,phase=1)))
    time.sleep(1)

    #### Project an image
    width = 640
    height = 480
    image = np.zeros([height, width, 3], np.uint8)
    for y in range(height):
        for x in range(0, width):
            image[y,x] = (
                255 * y / height , # Blue
                255 * x / width , # Green
                255 - 255 * y / height # Red
            )
    source = Source(format = Format.BGR888, width=width, height=height)
    scanner.SendTaskWithBuffer(6, V3Task.SetProjector, image.tobytes(),Projector(image=Image(source=source, target=Rect(100,100,640, 480))) )
    time.sleep(1)

    #### Turn OFF
    scanner.SendTask(7, V3Task.SetProjector, Projector(on=False))

except Exception as error:
    print('Error : ', error)
except:
    print('Error')

finally: 
    if scanner.IsConnected():
        scanner.Disconnect()