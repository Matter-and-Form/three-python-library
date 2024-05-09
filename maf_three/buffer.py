# buffer.py


from maf_three.task import Task


class Buffer:
    """Class representing a buffer."""

    Index: int
    """The index of the buffer."""

    totalBufferSize: int
    """The total size of the buffer that will be sent."""

    task:Task
    """The related task."""


    def __init__(self, bufferIndex:int,totalBufferSize:int, task:Task, Input = None):
        self.Index = bufferIndex
        self.totalBufferSize = totalBufferSize
        self.Task = task
