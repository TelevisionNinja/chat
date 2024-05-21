import socket
import sys


ip = '127.0.0.1'
port = 12000
address = (ip, port)
bufferSize = 1024


def main():
    # use tcp
    clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    try:
        clientSocket.connect(address)
    except:
        print('Please run the TTSServer.py file before running the TTSClient.py file')
        return

    text = sys.argv[1:]
    text = text[0]
    text = text.encode()

    clientSocket.send(text)
    clientSocket.close()


if __name__ == '__main__':
    main()
