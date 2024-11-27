from MF.V3.Task import Task as MF_V3_Task_Task
from google.protobuf import any_pb2 as _any_pb2


class Buffer:
    """*
    Generic buffer message for the Three Scanner.

    Some tasks require the server and/or client to transfer binary data.  In such cases the _buffer message_ is sent to inform the server/client what the data is and what task it belongs to.  The binary data it refers to is sent immediately following the buffer message.

    For example, `DownloadProject` requires the server to transfer a ZIP file containing the project data to the client.

    > First, the client sends the task request to the server:

    ```json
    {
    "Task":{
    "Index":1,
    "Type":"DownloadProject",
    "Input":5
    }
    }
    ```

    > The server sends the buffer message telling the client to expect a binary data transfer and what to do with it.  Note that the buffer message `Task` field echoes the task request, making it clear which request this data is a response to.

    ```json
    {
    "Buffer":{
    "Descriptor":"Project-5.zip",
    "Index":0,
    "Size":15682096,
    "Task":{
    "Index":1,
    "Type":"DownloadProject",
    "Input":5
    }
    }
    }
    ```

    > The server then sends the 15682096 byte data buffer of the project ZIP file.
    > Finally, the server sends a task completion message.

    ```json
    {
    "Task":{
    "Index":1,
    "Type":"DownloadProject"
    "Input":5,
    "State":"Completed"
    }
    }
    ```
    """
    def __init__(self, Index: int, Size: int, Task: MF_V3_Task_Task, Descriptor: _any_pb2 = None):
        # The zero-based index identifying the data buffer.
        self.Index = Index
        # The size of the incoming data buffer in bytes.
        self.Size = Size
        # The task associated with the data buffer.  This informs the client which request this data buffer corresponds to.
        self.Task = Task
        # Optional data buffer descriptor.  See each task definition for details.
        self.Descriptor = Descriptor


