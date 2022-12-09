from socket import *

import request
import response

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('localhost', 12000))
    serverSocket.listen(1)
    print('Server started')
    while True:
        connectionSocket, addr = serverSocket.accept()
        while True:
            b1 = connectionSocket.recv(1)
            opcode, length = request.decode_first_byte(b1)

if __name__ == "__main__":
    main()