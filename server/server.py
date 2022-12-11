from socket import *
import os
import sys

# Add parent directory to import list so we can include request and response modules
sys.path.append(os.path.join(sys.path[0], '..'))
import request
import response

debug = False

def main():
    if (len(sys.argv) > 1 and sys.argv[1] == '1'):
        global debug
        debug = True

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('localhost', 12000))
    serverSocket.listen(1)
    print('Server started')

    while True:
        connectionSocket, addr = serverSocket.accept()

        if debug:
            print("Client connected:", addr)

        while True:
            b1 = connectionSocket.recv(1)
            opcode, length = request.decode_first_byte(b1)

            if debug:
                print("Received request header", b1)

            if opcode == request.RequestType.PUT:
                handle_put(connectionSocket, length)
            elif opcode == request.RequestType.GET:
                handle_get(connectionSocket, length)
            elif opcode == request.RequestType.CHANGE:
                handle_change(connectionSocket, length)
            elif opcode == request.RequestType.HELP:
                handle_help(connectionSocket)
            else:
                handle_unknown(connectionSocket)

def handle_put(s: socket, filenameLength: int):
    fileName = s.recv(filenameLength).decode()
    fileSize = int.from_bytes(s.recv(4), 'big')
    fileData = s.recv(fileSize)
    with open(fileName, "wb") as f:
        f.write(fileData)
    s.send(response.encode_put_change_successful())
    if debug:
        print("Handled put for filename", fileName, "with data", fileData)

def handle_get(s: socket, filenameLength: int):
    fileName = s.recv(filenameLength).decode()
    try:
        with open(fileName, "rb") as f:
            content = f.read()
            contentLength = len(content)
            s.send(response.encode_get_successful(fileName, contentLength))
            s.send(content)
        if debug:
            print("Handled get request for ", fileName)
    except FileNotFoundError:
        s.send(response.encode_get_not_found())
        if debug:
            print("Failed get request for", fileName)

def handle_change(s: socket, oldFilenameLength: int):
    oldFilename = s.recv(oldFilenameLength).decode()
    newFilenameLength = int.from_bytes(s.recv(1), 'big')
    newFilename = s.recv(newFilenameLength).decode()
    try:
        os.rename(oldFilename, newFilename)
        s.send(response.encode_put_change_successful())
        print("Handled change request to rename", oldFilename, "to", newFilename)
    except OSError:
        s.send(response.encode_change_failed())
        print("Failed change request to rename ", oldFilename, " to ", newFilename)

def handle_help(s: socket):
    s.send(response.encode_help_response())
    print("Handled help request")

def handle_unknown(s: socket):
    s.send(response.encode_unknown_request_response())
    print("Handled unknown request")

if __name__ == "__main__":
    main()