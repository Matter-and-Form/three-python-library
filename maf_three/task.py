

from enum import Enum

from maf_three.V3Task import V3Task


class TaskState(str, Enum):

   
   Sent = 'Sent',
   """The task has been sent by the client."""

   Received = 'Received',
   """The task has been received by the server."""

   Started = 'Started',
   """The task started by the server."""

   Completed = 'Completed',
   """The task is completed by the server."""

   Cancelled = 'Cancelled',
   """The task has been cancelled by the client."""

   Failed = 'Failed',
   """The task has failed, A string describing the error is returned with the task."""

   Dropped = 'Dropped',
   """The task has not been received by the server, or task IDs were sent out of sequence."""

   Disconnected = 'Disconnected'
   """The client has been disconnected from the server before the task could finish."""

class Task:
   """
   Class representing a task.

   The typical lifecycle is :

   - Client creates the task.
   - Client sends it to the Server.
   - Server starts processing the task.
   - Server notifies the Client that the processing has started.
   - Server finishes processing the task.
   - Server notifies the Client that the processing is done.
   - Client handles an optional output associated with the task.
   """

   Index: int
   """The index of the task. Set by the client only."""

   Type:V3Task
   """The type of the task. Set by the client only."""

   Input = None
   """The input of the task. Set by the client only."""

   Output = None
   """The output of the task. Set by the server only."""

   State: TaskState | None
   """The state of the task. Set by the server only."""

   Progress: None
   """The progress of the task. Set by the server only."""

   Error: None
   """Error related to the task. Set by the server only."""

   def __init__(self, Index:int, Type:V3Task, Input=None, Output=None, State=None, Progress=None, Error=None ):
      self.Index = Index
      self.Type = Type

      self.Input = Input
      self.Output = Output

      self.State = State
      self.Progress = Progress
      self.Error = Error

   def __str__(self):
        return f'"{self.Index} - {self.Type}" State: {self.State}; Input: {self.Input}; Output: {self.Output}'