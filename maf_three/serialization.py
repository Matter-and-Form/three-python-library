# serialization.py

from array import *
import json

from google.protobuf.json_format import MessageToDict


def Serializer(object): 
    # Array is not JSON serializable => Convert to list
    if isinstance(object, array):
        return object.tolist()
    
    # Protobuf object
    if hasattr(object, "DESCRIPTOR"):
        dic = MessageToDict(
            object, 
            preserving_proto_field_name=True, 
            including_default_value_fields=True
        )
        return dict(filter(lambda tup:tup[1] is not None, dic.items()))
    
    # Our objects
    return dict(filter(lambda tup:tup[1] is not None, object.__dict__.items()))


def TO_JSON(object) -> str:
    """
    Serialize an object into a json string.
    
    Args: 
        object: the object to serialize.

    Returns:
        The string representing the object.

    """

    return json.dumps(
    object,
    default=Serializer,
    allow_nan=False)
