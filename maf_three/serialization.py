# import logging
from array import array
import json
from google.protobuf.json_format import MessageToDict
from enum import Enum

# Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

def Serializer(object, visited=None):
    if visited is None:
        visited = set()

    # logger.debug(f"Serializing object: {object} (id: {id(object)})")

   # Only track objects for circular references
    if isinstance(object, (dict, list, set, tuple, Enum)) or hasattr(object, '__dict__'):
        if id(object) in visited:
            return None
        visited.add(id(object))

    # Handle enums
    if isinstance(object, Enum):
        return object.name

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
        return dict(filter(lambda tup: tup[1] is not None, dic.items()))
    
    # Our objects
    if hasattr(object, '__dict__'):
        dic = dict(filter(lambda tup: tup[1] is not None, object.__dict__.items()))
        for key, value in dic.items():
            dic[key] = Serializer(value, visited)
        return dic

    # Handle other types if necessary
    return object

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
        allow_nan=False
    )