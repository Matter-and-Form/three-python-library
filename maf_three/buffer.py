



from maf_three.V3Task import V3Task
from maf_three.task import Task


class Buffer:
    def __init__(self, bufferIndex:int,totalBufferSize:int, task:Task, Input = None):
        self.Index = bufferIndex
        self.totalBufferSize = totalBufferSize
        self.Task = task
