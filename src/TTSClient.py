import socket
import sys


ip = '127.0.0.1'
port = 12000
address = (ip, port)
bufferSize = 1024
# use tcp
clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)


def main():
    try:
        clientSocket.connect(address)
    except:
        print('Please run the TTSServer.py file before running the TTSClient.py file')
        return

    filename = sys.argv[1:]
    filename = filename[1] # first arg is voice id
    text = ''

    with open(filename, 'r') as file:
        text = file.read()

    text = text.encode()

    clientSocket.send(text)
    clientSocket.close()


if __name__ == '__main__':
    main()
