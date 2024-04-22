

from typing import Any, Callable, Optional
import websocket
import json
import threading


from src.V3Task import V3Task
from src.task import Task


class Scanner:

    __bufferDescriptor = None

    def __init__(self,
        OnTask: Optional[Callable[[Task], None]],
        OnMessage: Optional[Callable[[str], None]],
        OnBuffer: Optional[Callable[[Any, bytes], None]],
        ):

        self.__connected = False

        self.OnTask = OnTask
        self.OnMessage = OnMessage
        self.OnBuffer = OnBuffer


    def Connect(self, URI:str):
        self.URI = URI

        print('Connecting to : ', URI)

        self.websocket = websocket.WebSocketApp(URI,
                              on_open=self.__OnOpen,
                              on_close=self.__OnClose,
                              on_error=self.__OnError,
                              on_message=self.__OnMessage,
                              )
        
        wst = threading.Thread(target=self.websocket.run_forever)
        wst.daemon = True
        wst.start()
        

    def Disconnect(self):
        self.websocket.close()

    def IsConnected(self)-> bool:
        return self.__connected

    """Websocket callbacks"""    

    def _callback(self, callback, *args) -> None:
        if callback:
                callback(self, *args)
        
    def __OnOpen(self, ws):
        self.__connected = True
        print('Connected to  : ', self.URI)

    def __OnClose(self, ws, close_status_code, close_msg):
        self.__connected = False
        print('Connection closed ', close_status_code, close_msg)

    def __OnError(self, ws, error):
        print('Error : ', error)

    def __OnMessage(self, ws, message):
        
        if isinstance(message, bytes):
            if self.OnBuffer:

                # wst = threading.Thread(target=self.OnBuffer, args=[self.__bufferDescriptor, message])
                # wst.daemon = True
                # wst.start()

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


    def SendTask(self, index:int, type:V3Task, input = None):

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
        


