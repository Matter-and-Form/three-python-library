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


    def Connect(self, URI:str, timeout=3) -> bool:

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
        while time.time() < start + timeout:
            if self.__isConnected: return True
            elif self.__error: raise Exception(self.__error)
            time.sleep(0.1)
        
        raise Exception('Connection timeout')
        
    def Disconnect(self) -> None:
        print('Disconnecting ...')
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
    def SendTask(self, index:int, type:V3Task, input = None) -> None:
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


