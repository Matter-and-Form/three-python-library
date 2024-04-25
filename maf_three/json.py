# json.py

from array import *
import json


def Serializer(object): 
    # Array is not JSON serializable => Convert to list
    if isinstance(object, array):
        return object.tolist()
        
    return dict(filter(lambda tup:tup[1] is not None, object.__dict__.items()))
    

def TO_JSON(object) -> str:
    return json.dumps(
    object,
    default=Serializer,
    allow_nan=False)
