# Projector

import sys
import os
import time
import numpy as np

# from maf_three.scanner import Scanner
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from maf_three.MF.V3.Tasks import SetProjector

from maf_three.scanner import Scanner

def main():

    try:
        # scanner = Scanner(OnTask=None, OnMessage=None, OnBuffer=None)
        # scanner.Connect("ws://matterandform.local:8081")

        #### Turn ON
        set_projector_request = SetProjector.Request(
            Index=1,
            Type="SetProjector",
            Input=SetProjector.Projector(on=True, brightness=1.0, color=[1, 1, 1])
        )
        #     Index=1,
        #     Type="SetProjector",
        #     Input=SetProjector.Projector(on=True, brightness=1.0, color=[1, 1, 1])
        # )        # scanner.SendTask(Task)

        # task.Projector.CopyFrom(Projector(on=True, brightness=1.0, color=[1,1,1]))
        # print("test2")
        # print(task)
        # scanner.SendTask(task)
        # time.sleep(1)

        # #### Project Red
        # print('Project Red')
        # scanner.SendTask(1, V3Task.SetProjector, Projector(color=[1,0,0]))
        # time.sleep(1)

        # #### Project Green
        # print('Project Green')
        # scanner.SendTask(2, V3Task.SetProjector, Projector(color=[0,1,0]))
        # time.sleep(1)

        # #### Project Blue
        # print('Project Blue')
        # scanner.SendTask(3, V3Task.SetProjector, Projector(color=[0,0,1]))
        # time.sleep(1)

        # #### Project Vertical Pattern
        # print('Project Vertical Pattern (Identical image columns)')
        # scanner.SendTask(4, V3Task.SetProjector, Projector(pattern=Projector.Pattern(orientation=Projector.Orientation.Vertical,frequency=4,phase=1)))
        # time.sleep(1)

        # #### Project Horizontal Pattern
        # print('Project Horizontal Pattern (Identical image rows)')
        # scanner.SendTask(5, V3Task.SetProjector, Projector(pattern=Projector.Pattern(orientation=Projector.Orientation.Horizontal,frequency=4,phase=1)))
        # time.sleep(1)

        # ### Project an image
        # print('Project Image')
        # width = 640
        # height = 480
        # image = np.zeros([height, width, 3], np.uint8)
        # for y in range(height):
        #     for x in range(0, width):
        #         image[y,x] = (
        #             255 * y / height , # Blue
        #             255 * x / width , # Green
        #             255 - 255 * y / height # Red
        #         )
        # source = Projector.Image.Source(format = Video.Format.BGR888, width=width, height=height, step=3*width, fixAspectRatio=True)
        # scanner.SendTaskWithBuffer(6, V3Task.SetProjector, image.tobytes(), Projector(image=Projector.Image(source=source, target=Rectangle(x=100,y=100,width=640, height=480))) )
        # time.sleep(1)

        # #### Turn OFF
        # print('Turn OFF')
        # scanner.SendTask(7, V3Task.SetProjector, Projector(on=False))

    except Exception as error:
        print('Error: ', error)
    except:
        print('Error')

    finally: 
        # if scanner.IsConnected():
        #     scanner.Disconnect()
        print('Finally')

if __name__ == "__main__":
    main()
