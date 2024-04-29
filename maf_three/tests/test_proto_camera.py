# test_proto_camera.py

import maf_three.Settings.Camera_pb2

def test_types():
    camera = maf_three.Settings.Camera_pb2.Camera()
    camera.autoExposure = False
    camera.exposure = 50000
    camera.digitalGain = 256
    camera.analogGain = 256
    camera.focus = 123

    raised = False
    try:
        camera.exposure = 'EXPOSURE'
    except TypeError:
        raised = True

    assert raised == True
