## @package maf_three
# @file scanner.py
# @brief Scanner class to wrap websocket connection
# @date 2024-04-22
# @copyright © 2024 Matter and Form. All rights reserved.

from typing import Any, Callable, Optional, List

import websocket
import json
import threading
import time

from MF.V3 import Task, TaskState
from MF.V3.Tasks.SetProjector import SetProjector, Settings_Projector

from maf_three import __version__
from maf_three.serialization import TO_JSON
from maf_three.buffer import Buffer


class Scanner:
    """
    Main class to manage and communicate with the Matter and Form THREE 3D Scanner via websocket.

    Attributes:
        * OnTask (Callable[[Task], None]): Function to handle tasks.
        * OnMessage (Callable[[str], None]): Function to handle messages.
        * OnBuffer (Callable[[Any, bytes], None]): Function to handle buffer data.
    """
    
    __bufferDescriptor = None
    __error = None
    __taskIndex:int = 0
    __tasks:List[Task] = []


    def __init__(self,
        OnTask: Optional[Callable[[Task], None]],
        OnMessage: Optional[Callable[[str], None]],
        OnBuffer: Optional[Callable[[Any, bytes], None]],
        ):
        """
        Initializes the Scanner object.

        Args:
            * OnTask (Optional[Callable[[Task], None]]): Function to handle tasks, default is None.
            * OnMessage (Optional[Callable[[str], None]]): Function to handle messages, default is None.
            * OnBuffer (Optional[Callable[[Any, bytes], None]]): Function to handle buffer data, default is None.
        """
        self.__isConnected = False

        self.OnTask = OnTask
        self.OnMessage = OnMessage
        self.OnBuffer = OnBuffer
        
        self.__task_return_event = threading.Event()

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
                self.OnBuffer(self.__bufferDescriptor, message)
                self.__bufferDescriptor = None 
        else:
            obj = json.loads(message)              
        
            # Task
            if 'Task' in obj:
                # Create the task from the message
                task = Task(**obj['Task'])

                # Find the original task for reference
                inputTask = self.__FindTaskWithIndex(task.Index)
                assert inputTask

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
                self.__bufferDescriptor = obj['Buffer']
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

        # Send the task
        
        self.__task_return_event.clear()
        
        # Append the task
        self.__tasks.append(task)

        if buffer == None:
            task = self.__SendTask(task)
        else:
            task = self.__SendTaskWithBuffer(task, buffer)

        if task.Output:
            # Wait for response
            self.__task_return_event.wait()

        self.__tasks.remove(task)

        return task
    
    # Send a task to the scanner
    def __SendTask(self, task) -> Any:
        assert self.__isConnected
        
        # Serialize the task
        message = TO_JSON(task.Input)
        
        # Build and send the message
        message = '{"Task":' + message + '}'
        #print('Message: ', message)   
        self.websocket.send(message)

        return task

    # Send a task with its buffer to the scanner
    def __SendTaskWithBuffer(self, task:Task, buffer:bytes) -> Any:
        assert self.__isConnected

        # Send the task
        task = self.__SendTask(task.Input)

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

        return task
    
    def __FindTaskWithIndex(self, index:int) -> Task:
        # Find the task in the list
        for i, t in enumerate(self.__tasks):
            if t.Index == index:
                return t
                break
        return None
        
    def SetProjector(self, on:bool, brightness:float, color:List[float]) -> Task:
        
        """
        Sets the projector settings.

        Args:
            * on (bool): True to turn the projector on, False to turn it off.
            * brightness (float): The brightness of the projector, between 0.0 and 1.0.
            * color ([float]): The RGB color of the projector, as a list of three floats between 0.0 and 1.0.

        Returns:
            Task: The task object that was sent.
        """
        set_projector_request = SetProjector.Request(
            Index=self.__taskIndex,
            Type="SetProjector",
            Input=Settings_Projector(on=on, brightness=brightness, color=color)
        )
        set_projector_response = SetProjector.Response(
            Index=self.__taskIndex,
            Type="SetProjector"
        )
        
        task = Task(Index=self.__taskIndex, Type="SetProjector", Input=set_projector_request, Output=set_projector_response)

        self.__taskIndex += 1

        print(self.SendTask(task))
        
        return 

# Main function to run the code
if __name__ == "__main__":
    def on_task(task):
        print(f"Task received: {task}")

    def on_message(message):
        print(f"Message received: {message}")

    def on_buffer(buffer, data):
        print(f"Buffer received: {data}")

    scanner = Scanner(OnTask=on_task, OnMessage=on_message, OnBuffer=on_buffer)
    scanner.Connect("ws://matterandform.local:8081")

    # Set the projector settings for debugging
    scanner.SetProjector(on=True, brightness=1.0, color=[1, 1, 1])
    time.sleep(1)
    scanner.SetProjector(on=False, brightness=1.0, color=[1, 1, 1])
    time.sleep(1)
    scanner.SetProjector(on=True, brightness=0.0, color=[1, 1, 1])
    time.sleep(1)
    scanner.SetProjector(on=True, brightness=1.0, color=[1, 0, 0])
    time.sleep(1)

    scanner.Disconnect()