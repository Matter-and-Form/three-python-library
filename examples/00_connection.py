# 00_connection.py

from three_api.scanner import Scanner
from three_api.task import Task

try:
    scanner = Scanner(OnTask=None, OnMessage=None, OnBuffer=None)
    scanner.Connect("ws://matterandform.local:8081")

except Exception as error:
    print('Scanner error : ', error)
except:
    print('Scanner error')

finally: 
    if scanner.IsConnected():
        scanner.Disconnect()