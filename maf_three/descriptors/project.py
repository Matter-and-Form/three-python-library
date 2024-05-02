import datetime

from enum import Enum

class Project:
    def __init__(self, index:int, name:str, modified:list, size:int):
        self.index = index
        self.name = name
        self.modified = datetime.datetime(modified[0], modified[1] + 1, modified[2], modified[3], modified[4], modified[5])
        self.size = size

    def __str__(self):
        return f'Project: {self.index} - {self.name}\t {self.size} b\t {self.modified}'
    


