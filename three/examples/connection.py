# Connection

from three.scanner import Scanner

def main():
    try:
        scanner = Scanner(OnTask=None, OnMessage=None, OnBuffer=None)
        scanner.Connect("ws://matterandform.local:8081")

    except Exception as error:
        print('Error: ', error)
    except:
        print('Error: Unknown')

    finally: 
        if scanner.IsConnected():
            scanner.Disconnect()

if __name__ == "__main__":
    main()
