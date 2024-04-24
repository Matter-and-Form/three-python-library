## @package three_api
# @file scanner.py
# @brief Scanner class to wrap websocket connection
# @date 2024-04-22
# @copyright © 2024 Matter and Form. All rights reserved.

from typing import Any, Callable, Optional

import websocket
import json
import threading
import time


from three_api.V3Task import V3Task
from three_api.task import Task
from three_api.buffer import Buffer


class Scanner:

    __bufferDescriptor = None
    __error = None

    def __init__(self,
        OnTask: Optional[Callable[[Task], None]],
        OnMessage: Optional[Callable[[str], None]],
        OnBuffer: Optional[Callable[[Any, bytes], None]],
        ):

        self.__isConnected = False

        self.OnTask = OnTask
        self.OnMessage = OnMessage
        self.OnBuffer = OnBuffer


    def Connect(self, URI:str, timeoutSec=5) -> bool:

        print('Connecting to : ', URI)
        self.__URI = URI
        self.__isConnected = False
        self.__error = None

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
            if self.__isConnected: return True
            elif self.__error: raise Exception(self.__error)
            time.sleep(0.1)
        
        raise Exception('Connection timeout')
        
    def Disconnect(self) -> None:
        self.websocket.close()

    def IsConnected(self)-> bool:
        return self.__isConnected
    
    def __callback(self, callback, *args) -> None:
        if callback:
                callback(self, *args)
 
    # Called when the connection is opened
    def __OnOpen(self, ws) -> None:
        self.__isConnected = True
        print('Connected to  : ', self.__URI)

    # Called when the connection is closed
    def __OnClose(self, ws, close_status_code, close_msg):
        if self.__isConnected:
            print('Disconnected')
        self.__isConnected = False

    # Called when an error happens
    def __OnError(self, ws, error) -> None:
        if self.__isConnected:
            print('Error : ', error)    
        else:
            self.__error = error
        
    # Called when a message arrives on the connection
    def __OnMessage(self, ws, message) -> None:
        
        # Bytes ?
        if isinstance(message, bytes):
            if self.OnBuffer:
                self.OnBuffer(self.__bufferDescriptor, message)
                self.__bufferDescriptor = None 
        else:
            obj = json.loads(message)              
        
            # Task
            if 'Task' in obj:
                if self.OnTask:
                    self.OnTask(Task(**obj['Task']))
            # Buffer
            elif 'Buffer' in obj:
                self.__bufferDescriptor = obj['Buffer']
            # Message
            elif 'Message' in obj:
                if self.OnMessage:
                    self.OnMessage(obj)

    # Send a task to the scanner
    def SendTask(self, index:int, type:V3Task, input = None) -> Task:
        assert self.__isConnected
        
        # Create the task
        task = Task(index, type, input)

        # Serialize the task
        message = json.dumps(
            task,
            default=lambda o: dict((key, value) for key, value in o.__dict__.items() if value != None),
            allow_nan=False)
        
        # Build and send the message
        message = '{"Task":' + message + '}'
        #print('Message : ', message)   
        self.websocket.send(message)

        return task

    def SendTaskWithBuffer(self, index:int, type:V3Task, buffer:bytes, input = None):
        assert self.__isConnected

        # Send the task
        task = self.SendTask(index, type, input)

        # Build the buffer descriptor
        bufferSize = len(buffer)
        bufferDescriptor = Buffer(0, bufferSize, task)

        # Serialize the buffer descriptor
        bufferMessage = json.dumps(
            bufferDescriptor,
            default=lambda o: dict((key, value) for key, value in o.__dict__.items() if value != None),
            allow_nan=False)

        # Send the buffer descriptor
        bufferMessage = '{"Buffer":' + bufferMessage + '}'
        self.websocket.send(bufferMessage)

        # Send the buffer
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


