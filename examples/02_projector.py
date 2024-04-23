# Projector

from three_api.buffer import Buffer
from three_api.scanner import Scanner
from three_api.settings.projector import Image, Orientation, Pattern, Projector, Rect, Source
from three_api.settings.video import Format
from three_api.task import Task, TaskState
from three_api.V3Task import V3Task

import time
import numpy as np
import cv2

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
    #image = np.zeros([300, 200, 3], np.uint8)
    image = cv2.imread('image.png')
    source = Source(format = Format.BGR888, width=image.shape[1], height=image.shape[0])
    task = scanner.SendTask(6, V3Task.SetProjector, Projector(image=Image(source=source, target=Rect(100,100,600, 400))))
    scanner.SendBuffer(task, image.tobytes())
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