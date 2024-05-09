# test_proto_camera.py

from MF.V3.Settings.Camera import Camera

from google.protobuf.json_format import MessageToJson, Parse

def test_types():
    camera = Camera()
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

def test_serialization():
    
    # Create cameraA object
    cameraA = Camera()
    cameraA.autoExposure = False
    cameraA.exposure = 50000
    cameraA.digitalGain = 256
    cameraA.analogGain = 256
    
    # Serialize cameraA to json
    cameraA_json = MessageToJson(cameraA)

    # Build cameraB from the cameraA json
    cameraB = Camera()
    cameraB = Parse(cameraA_json, cameraB)
    
    # Serialize cameraB to json
    cameraB_json = MessageToJson(cameraB)

    # Compare the two objects and their json serializations
    assert cameraA == cameraB
    assert cameraA_json == cameraB_json
