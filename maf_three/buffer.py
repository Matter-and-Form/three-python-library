


from maf_three.task import Task


class Buffer:
    def __init__(self, bufferIndex:int,totalBufferSize:int, task:Task, Input = None):
        self.Index = bufferIndex
        self.totalBufferSize = totalBufferSize
        self.Task = task
