

from enum import Enum

from maf.V3Task import V3Task


class TaskState(str, Enum):

   # The task has been sent by the client. 
   Sent = 'Sent',

   # The task has been received by the server. 
   Received = 'Received',

   # The task started by the server. 
   Started = 'Started',

   # The task is completed by the server. 
   Completed = 'Completed',

   # The task has been cancelled by the client. 
   Cancelled = 'Cancelled',

   # The task has failed, A string describing the error is returned with the task. 
   Failed = 'Failed',

   # The task has not been received by the server, or task IDs were sent out of sequence. 
   Dropped = 'Dropped',

   # The client has been disconnected from the server before the task could finish. 
   Disconnected = 'Disconnected'

class Task:
   def __init__(self, Index, Type:V3Task, Input=None, Output=None, State=None, Progress=None, Error=None ):
      self.Index = Index
      self.Type = Type

      self.Input = Input
      self.Output = Output

      self.State = State
      self.Progress = Progress
      self.Error = Error

   def __str__(self):
        return f'Task : {self.Index} - {self.Type} ; {self.Input} ; {self.Output}'