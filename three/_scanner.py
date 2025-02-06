## @package three
# @file scanner.py
# @brief Scanner class to wrap websocket connection. This file will be copied and amended with the three methods.
# @date 2024-11-27
# @copyright © 2024 Matter and Form. All rights reserved.

from typing import Any, Callable, Optional, List

import websocket
import json
import threading
import time

from MF.V3 import Task, TaskState, Buffer

from three import __version__
import three.MF
from three.serialization import TO_JSON
from three.MF.V3.Buffer import Buffer

class Scanner:
    """
    Main class to manage and communicate with the Matter and Form THREE 3D Scanner via websocket.

    Attributes:
        * OnTask (Optional[Callable[[Task], None]]): Callback for any task related messages, default is None. Will fire for task complete, progress, and error.
        * OnMessage (Optional[Callable[[str], None]]): Callback function to handle messages, default is None. Messages are any calls related to the system that are not tasks or buffers. Eg. {"Message":{"HasTurntable":true}}
        * OnBuffer (Optional[Callable[[Any, bytes], None]]): Callback Function to handle buffer data, default is None. Buffers can be image or scan data. These are binary formats that are sent separately from tasks. Buffers will contain a header that describes the buffer data size. Please note that websocket buffers are limited in size and need to be sent in chunks.
    """
    
    __bufferDescriptor = None
    __buffer = None
    __error = None
    __taskIndex:int = 0
    __tasks:List[Task] = []


    def __init__(self,
        OnTask: Optional[Callable[[Task], None]] = None,
        OnMessage: Optional[Callable[[str], None]] = None,
        OnBuffer: Optional[Callable[[Any, bytes], None]] = None,
        ):
        """
        Initializes the Scanner object.

        Args:
            * OnTask (Optional[Callable[[Task], None]]): Callback for any task related messages, default is None. Will fire for task complete, progress, and error.
            * OnMessage (Optional[Callable[[str], None]]): Callback function to handle messages, default is None. Messages are any calls related to the system that are not tasks or buffers. Eg. {"Message":{"HasTurntable":true}}
            * OnBuffer (Optional[Callable[[Any, bytes], None]]): Callback Function to handle buffer data, default is None. Buffers can be image or scan data. These are binary formats that are sent separately from tasks. Buffers will contain a header that describes the buffer data size. Please note that websocket buffers are limited in size and need to be sent in chunks.
        """
        self.__isConnected = False

        self.OnTask = OnTask
        self.OnMessage = OnMessage
        self.OnBuffer = OnBuffer
        
        self.__task_return_event = threading.Event()
        
        # Dynamically add methods from Three to Scanner
        # self._add_three_methods()

    # def _add_three_methods(self):
    #     """
    #     Dynamically adds functions from the three_methods module to the Scanner class.
    #     """
    #     for name, func in inspect.getmembers(Three, predicate=inspect.isfunction):
    #         if not name.startswith('_'):
    #             setattr(self, name, func.__get__(self, self.__class__))


    def Connect(self, URI:str, timeoutSec=5) -> bool:
        """
        Attempts to connect to the scanner using the specified URI and timeout.

        Args:
            * URI (str): The URI of the websocket server.
            * timeoutSec (int): Timeout in seconds, default is 5.

        Returns:
            bool: True if connection is successful, raises Exception otherwise.

        Raises:
            Exception: If connection fails within the timeout or due to an error.
        """
        print('Connecting to: ', URI)
        self.__URI = URI
        self.__isConnected = False
        self.__error = None

        self.__serverVersion__= None

        self.websocket = websocket.WebSocketApp(self.__URI,
                              on_open=self.__OnOpen,
                              on_close=self.__OnClose,
                              on_error=self.__OnError,
                              on_message=self.__OnMessage,
                              )
        
        wst = threading.Thread(target=self.websocket.run_forever)
        wst.daemon = True
        wst.start()

        # Wait for connection
        start = time.time()
        while time.time() < start + timeoutSec:
            if self.__isConnected:
                # Not checking versions => return True
                    return True
            elif self.__error:
                raise Exception(self.__error)
            time.sleep(0.1)
        
        raise Exception('Connection timeout')
        
    def Disconnect(self) -> None:
        """
        Close the websocket connection.
        """
        if self.__isConnected:
            # Close the connection
            self.websocket.close()
            # Wait for the connection to be closed.
            while self.__isConnected:
                time.sleep(0.1)

    def IsConnected(self)-> bool:
        """
        Checks if the scanner is currently connected.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self.__isConnected
    
    def __callback(self, callback, *args) -> None:
        if callback:
                callback(self, *args)

    # Called when the connection is opened
    def __OnOpen(self, ws) -> None:
        """
        Callback function for when the websocket connection is successfully opened.

        Prints a success message to the console.

        Args:
            ws: The websocket object.
        """
        self.__isConnected = True
        print('Connected to: ', self.__URI)

    # Called when the connection is closed
    def __OnClose(self, ws, close_status_code, close_msg):
        """
        Callback function for when the websocket connection is closed.

        Prints a disconnect message to the console.

        Args:
            ws: The websocket object.
            close_status_code: The code indicating why the websocket was closed.
            close_msg: Additional message about why the websocket was closed.
        """
        if self.__isConnected:
            print('Disconnected')
        self.__isConnected = False

    # Called when an error happens
    def __OnError(self, ws, error) -> None:
        """
        Callback function for when an error occurs in the websocket connection.

        Prints an error message to the console and stores the error for reference.

        Args:
            ws: The websocket object.
            error: The error that occurred.
        """
        if self.__isConnected:
            print('Error: ', error)    
        else:
            self.__error = error
        
    # Called when a message arrives on the connection
    def __OnMessage(self, ws, message) -> None:
        """
        Callback function for handling messages received via the websocket.

        Determines the type of message received (Task, Buffer, or general Message) and
        triggers the corresponding handler function if one is set.

        Args:
            ws: The websocket object.
            message: The raw message received, which can be either a byte string or a JSON string.
        """
        # Bytes ?
        if isinstance(message, bytes):
            if self.OnBuffer:
                
                if self.__buffer:
                    self.__buffer += message
                else:
                    self.__buffer = message
                if self.__bufferDescriptor.Size == len(self.__buffer):
                    self.OnBuffer(self.__bufferDescriptor, message)
                    self.__bufferDescriptor = None 
                    self.__buffer = None
        else:
            obj = json.loads(message)              
        
            # Task
            if 'Task' in obj:
                # Create the task from the message
                task = Task(**obj['Task'])
                
                if (task.Progress):
                    # Extract the first (and only) item from the task.Progress dictionary
                    # TODO Duct tape fix due to schema weirdness for progress
                    key, process = next(iter(task.Progress.items()))
                    task.Progress = type('Progress', (object,), {
                        'current': process["current"],
                        'step': process["step"],
                        'total': process["total"]
                    })()

                # Find the original task for reference
                inputTask = self.__FindTaskWithIndex(task.Index)
                if inputTask == None:
                    raise Exception('Task not found')
                    
                if task.Error:
                    inputTask.Error = task.Error
                    self.__OnError(self.websocket, task.Error)
                    self.__task_return_event.set()
                    
                # If assigned => Call the handler
                if self.OnTask:
                    self.OnTask(task)
                
                
                # If waiting for a response, set the response and notify
                if (task.State == TaskState.Completed.value):
                    if task.Output:
                        inputTask.Output = task.Output
                    self.__task_return_event.set()
                elif (task.State == TaskState.Failed.value):
                    inputTask.Error = task.Error
                    self.__task_return_event
                    
            # Buffer
            elif 'Buffer' in obj:
                self.__bufferDescriptor = Buffer(**obj['Buffer'])
                self.__buffer = None    
            # Message
            elif 'Message' in obj:
                if self.OnMessage:
                    self.OnMessage(obj)

    def SendTask(self, task, buffer:bytes = None) -> Any:
        """
        Sends a task to the scanner.
        Tasks are general control requests for the scanner. (eg. Camera exposure, or Get Image)

        Creates a task, serializes it, and sends it via the websocket.

        Args:
            * task (Task): The task to send.
            * buffer (bytes): The buffer data to send, default is None.

        Returns:
            Any: The task object that was sent.

        Raises:
            AssertionError: If the connection is not established.
        """
        assert self.__isConnected

        # Update the index
        task.Index = self.__taskIndex
        task.Input.Index = self.__taskIndex
        self.__taskIndex += 1

        # Send the task
        self.__task_return_event.clear()
        
        # Append the task
        self.__tasks.append(task)

        if buffer == None:
            self.__SendTask(task)
        else:
            self.__SendTaskWithBuffer(task, buffer)

        if task.Output:
            # Wait for response
            self.__task_return_event.wait()

        self.__tasks.remove(task)

        return task
    
    # Send a task to the scanner
    def __SendTask(self, task):
        assert self.__isConnected

        # Serialize the task
        message = TO_JSON(task.Input)
        
        # Build and send the message
        message = '{"Task":' + message + '}'
        print('Message: ', message)

        self.websocket.send(message)

    # Send a task with its buffer to the scanner
    def __SendTaskWithBuffer(self, task:Task, buffer:bytes):
        assert self.__isConnected

        # Send the task
        self.__SendTask(task)

        # Build the buffer descriptor
        bufferSize = len(buffer)
        bufferDescriptor = Buffer(0, bufferSize, task)

        # Serialize the buffer descriptor
        bufferMessage = TO_JSON(bufferDescriptor)

        # Send the buffer descriptor
        bufferMessage = '{"Buffer":' + bufferMessage + '}'
        self.websocket.send(bufferMessage)

        # The maximum websocket payload size is 32 MB.
        MAX_SIZE = 32000000
        sentSize = 0

        # Send all the sub-payloads of the maximum payload size.
        while sentSize + MAX_SIZE < bufferSize:
            self.websocket.send(buffer[sentSize:sentSize + MAX_SIZE], websocket.ABNF.OPCODE_BINARY)
            sentSize += MAX_SIZE

        # Send the remaining data.
        if sentSize < bufferSize:
            self.websocket.send(buffer[sentSize:bufferSize], websocket.ABNF.OPCODE_BINARY)
    
    def __FindTaskWithIndex(self, index:int) -> Task:
        # Find the task in the list
        for i, t in enumerate(self.__tasks):
            if t.Index == index:
                return t
                break
        return None