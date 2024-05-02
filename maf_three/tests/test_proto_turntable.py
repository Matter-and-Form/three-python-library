# test_proto_camera.py

import maf_three.MF.V3.Settings.Turntable_pb2

def test_types():
    turntable = maf_three.MF.V3.Settings.Turntable_pb2.Turntable()
    turntable.use = True
    turntable.steps = 10
    turntable.sweep = 360

    raised = False
    try:
        turntable.use = 'USE_TURNTABLE'
    except TypeError:
        raised = True

    assert raised == True
