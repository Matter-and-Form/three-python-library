



from three_api.V3Task import V3Task
from three_api.task import Task


class Buffer:
    def __init__(self, bufferIndex:int,totalBufferSize:int, task:Task, Input = None):
        self.Index = bufferIndex
        self.totalBufferSize = totalBufferSize
        self.Task = task
