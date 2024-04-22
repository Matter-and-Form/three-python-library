import datetime

from enum import Enum

class Project:
    def __init__(self, index:int, name:str, modified:list, size:int):
        self.index = index
        self.name = name
        self.modified = datetime.datetime(modified[0], modified[1] + 1, modified[2], modified[3], modified[4], modified[5])
        self.size = size

    def __str__(self):
        return f'Project : {self.index} - {self.name}\t {self.size} b\t {self.modified}'
    

class Codec(str, Enum):
    # The frames coming from the Scanner are streaming in RAW format.
    RAW = 'RAW',

    # The frames coming from the Scanner are encoded in JPEG format.
    JPEG = 'JPEG',

    # The frames coming from the Scanner are encoded in H264 format.
    H264 = 'H264'

class Format(str, Enum):
    # BGR 24-bit.
    BGR888 = 'RGB888',

    # YUV 420 planar.
    YUV420 = 'YUV420'
