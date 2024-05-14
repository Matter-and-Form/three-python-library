## @package maf_three
# @file scanner.py
# @brief Scanner class to wrap websocket connection
# @date 2024-04-22
# @copyright © 2024 Matter and Form. All rights reserved.

from typing import Any, Callable, Optional

import websocket
import json
import threading
import time

from maf_three import __version__
from maf_three.V3Task import V3Task
from maf_three.serialization import TO_JSON
from maf_three.task import Task, TaskState
from maf_three.buffer import Buffer

from MF.V3.Descriptors.Software import Software


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


    def Connect(self, URI:str, timeoutSec=5, checkVersionsCompatibility=True) -> bool:
        """
        Attempts to connect to the scanner using the specified URI and timeout.

        Args:
            * URI (str): The URI of the websocket server.
            * timeoutSec (int): Timeout in seconds, default is 5.
            * checkVersionsCompatibility (bool): If True, right after the client connects to the server, check if the versions are compatible.

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
        self.__checkVersionsCompatibility__ = checkVersionsCompatibility

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
                if not checkVersionsCompatibility:
                    return True
                else:
                    # Request the server version
                    self.SendTask(0, V3Task.SoftwareVersionInstalled, 'three-server')
                    # Wait for the reply
                    while self.__serverVersion__ == None:
                        time.sleep(0.1)
                    # Compare the versions
                    if str(self.__serverVersion__.major) != __version__.split('.')[0]:
                        raise Exception(
                            'Major versions of Python library and Server mismatch.\n'+
                            '* Server:    '+ str(self.__serverVersion__.major)+ '.'+str(self.__serverVersion__.minor)+'.'+str(self.__serverVersion__.patch)+'\n'
                            '* maf_three: '+ __version__+'\n'+
                            'Please update your python library: pip3 install --upgrade --no-cache-dir maf_three')            
                    # Major versions match
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

                # Are we checking versions compatibility ?
                if self.__checkVersionsCompatibility__ and task.Type == V3Task.SoftwareVersionInstalled and task.State == TaskState.Completed:
                    self.__serverVersion__ = Software.Version(**task.Output)
                    self.__checkVersionsCompatibility__ = False

                # If assigned => Call the handler
                elif self.OnTask:
                    self.OnTask(task)
                    
            # Buffer
            elif 'Buffer' in obj:
                self.__bufferDescriptor = obj['Buffer']
            # Message
            elif 'Message' in obj:
                if self.OnMessage:
                    self.OnMessage(obj)

    # Send a task to the scanner
    def SendTask(self, index:int, type:V3Task, input = None) -> Task:
        """
        Sends a task to the scanner.
        Tasks are general control requests for the scanner. (eg. Camera exposure, or Get Image)

        Creates a task, serializes it, and sends it via the websocket.

        Args:
            * index (int): The index of the task.
            * type (V3Task): The type of the task.
            * input: Additional input for the task, default is None.

        Returns:
            Task: The task object that was sent.

        Raises:
            AssertionError: If the connection is not established.
        """
        assert self.__isConnected
        
        # Create the task
        task = Task(index, type, input)

        # Serialize the task
        message = TO_JSON(task)
        
        # Build and send the message
        message = '{"Task":' + message + '}'
        #print('Message: ', message)   
        self.websocket.send(message)

        return task

    # Send a task with its buffer to the scanner
    def SendTaskWithBuffer(self, index:int, type:V3Task, buffer:bytes, input = None) -> Task:
        """
        Sends a task along with its associated buffer to the scanner.
        This call is used to send data to the scanner, like an image to be projected by the projector. 
        An appropriate task must be sent with the buffer, or the buffer will be ignored.
        
        The task is serialized, and sent to the scanner, followed by the buffer.
        
        Args:
            * index (int): The index of the task.
            * type (V3Task): The type of the task.
            * buffer (bytes): The buffer data to send.
            * input: Additional input for the task, default is None.

        Returns:
            Task: The task object that was sent.

        Raises:
            AssertionError: If the connection is not established.
        """
        assert self.__isConnected

        # Send the task
        task = self.SendTask(index, type, input)

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

