from socket import *
import os
import sys

# Add parent directory to import list so we can include request and response modules
sys.path.append(os.path.join(sys.path[0], '..'))
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
            if opcode == request.RequestType.PUT:
                handle_put(connectionSocket, length)
            elif opcode == request.RequestType.GET:
                handle_get(connectionSocket, length)
            elif opcode == request.RequestType.CHANGE:
                handle_change(connectionSocket, length)
            elif opcode == request.RequestType.HELP:
                handle_help(connectionSocket)
            else:
                connectionSocket.send(response.encode_unknown_request_response())

def handle_put(s: socket, filenameLength: int):
    fileName = s.recv(filenameLength).decode()
    fileSize = int.from_bytes(s.recv(4), 'big')
    fileData = s.recv(fileSize)
    with open(fileName, "wb") as f:
        f.write(fileData)
    s.send(response.encode_put_change_successful())

def handle_get(s: socket, filenameLength: int):
    fileName = s.recv(filenameLength).decode()
    try:
        with open(fileName, "rb") as f:
            content = f.read()
            contentLength = len(content)
            s.send(response.encode_get_successful(fileName, contentLength))
            s.send(content)
    except FileNotFoundError:
        s.send(response.encode_get_not_found())

def handle_change(s: socket, oldFilenameLength: int):
    oldFilename = s.recv(oldFilenameLength).decode()
    newFilenameLength = int.from_bytes(s.recv(1), 'big')
    newFilename = s.recv(newFilenameLength).decode()
    try:
        os.rename(oldFilename, newFilename)
        s.send(response.encode_put_change_successful())
    except OSError:
        s.send(response.encode_change_failed())

def handle_help(s: socket):
    s.send(response.encode_help_response())

if __name__ == "__main__":
    main()