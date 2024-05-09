# test_proto_turntable.py

from MF.V3.Settings.Turntable import Turntable

def test_types():
    turntable = Turntable()
    turntable.use = True
    turntable.steps = 10
    turntable.sweep = 360

    raised = False
    try:
        turntable.use = 'USE_TURNTABLE'
    except TypeError:
        raised = True

    assert raised == True
