# Connection

from maf_three.scanner import Scanner

try:
    scanner = Scanner(OnTask=None, OnMessage=None, OnBuffer=None)
    scanner.Connect("ws://matterandform.local:8081")

except Exception as error:
    print('Error : ', error)
except:
    print('Error')

finally: 
    if scanner.IsConnected():
        scanner.Disconnect()