# Authors: Ben Hitterman (40174961), Matthew Faigan (40175089)
# Purpose: Client program that accepts user commands then sends a message to the server and receives a response
# We certify that this submission is the original work of members of the group and meets the Faculty's Expectations of Originality.

import os
from socket import *
import sys

# Add parent directory to import list so we can include request and response modules
sys.path.append(os.path.join(sys.path[0], '..'))
import request
import response

#server linking to client format: python3file ipAddress portNumber debugMode

#retrive server ip
serverIpAddress = sys.argv[1]
#retrive server port
serverPort = int(sys.argv[2])
#for Debug Mode
if (sys.argv[3] == '0'):
    debug = False
elif (sys.argv[3] == '1'):
    debug = True

#creating and connecting socket (establishing connection)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIpAddress, serverPort))
print('Session has been established')


def put(fileName):
    if os.path.isfile(fileName):
        requestMessage = request.encode_put(fileName, os.path.getsize(fileName))
        clientSocket.send(requestMessage)

        with open(fileName, 'rb') as file:
            fileData = file.read()
            print(len(fileData))
            clientSocket.send(fileData)

        receivedData = clientSocket.recv(1)

        if debug:
            print("Request sent in Debug mode:", requestMessage)
            print("Data sent in Debug mode:", fileData)
            print("Response received in Debug mode:", receivedData)

        opcoderecvd, lengthrecvd = response.decode_first_byte(receivedData)
        if opcoderecvd == response.ResponseType.PUT_CHANGE:
            print(fileName + " has been uploaded successfully")
        else:
            print(fileName + " not sent successfully")

    else:
        print(fileName + " does not exist")


def get(fileName):
    requestMessage = request.encode_get(fileName)
    clientSocket.send(requestMessage)

    receivedData = clientSocket.recv(1)

    if debug:
        print("Request sent in Debug mode: ", requestMessage)
        print("Data received in Debug mode: ", receivedData)

    opcoderecvd, lengthrecvd = response.decode_first_byte(receivedData)
    if opcoderecvd == response.ResponseType.GET:
        fileNameReceived = clientSocket.recv(lengthrecvd).decode()
        if fileName != fileNameReceived:
            print("File name not found")
            return
        fileSize = int.from_bytes(clientSocket.recv(4), 'big')

        fileData = b''
        bytesRead = 0
        while bytesRead < fileSize:
            bytesRemaining = fileSize - bytesRead
            if bytesRemaining > 4096:
                buf = clientSocket.recv(4096)
                fileData += buf
                bytesRead += len(buf)
            else:
                buf = clientSocket.recv(bytesRemaining)
                fileData += buf
                bytesRead += len(buf)

        #writing file
        with open(fileName, 'wb') as file:
            file.write(fileData)

        if debug:
            print("File data received in Debug mode: ", fileData)

        print(fileName + " has been downloaded successfully")
    
    elif opcoderecvd == response.ResponseType.ERR_NOT_FOUND:
        print(fileName + " not found")


def change(oldFileName, newFileName):
    requestMessage = request.encode_change(oldFileName, newFileName)
    clientSocket.send(requestMessage)

    receivedData = clientSocket.recv(1)

    if debug:
        print("Request sent in Debug mode: ", requestMessage)
        print("Data received in Debug mode: ", receivedData)

    opcoderecvd, lengthrecvd = response.decode_first_byte(receivedData)
    if opcoderecvd == response.ResponseType.PUT_CHANGE:
        print(oldFileName + " has been changed to " + newFileName + " successfully")
    elif opcoderecvd == response.ResponseType.ERR_CHANGE_FAILED:
        print(oldFileName + " not changed successfully")


def help():
    requestMessage = request.encode_help()
    clientSocket.send(requestMessage)

    receivedData = clientSocket.recv(1)

    if debug:
        print("Request sent: ", requestMessage)
        print("Data received: ", receivedData)

    opcoderecvd, lengthrecvd = response.decode_first_byte(receivedData)
    if opcoderecvd == response.ResponseType.HELP:
        print(clientSocket.recv(lengthrecvd).decode()) #printing 5 commands fetched from server
    else:
        print("Help not found")

def unknownRequest(request):
    firstByte = request.encode()
    clientSocket.send(firstByte)

    receivedData = clientSocket.recv(1)

    if debug:
        print("Request sent in Debug mode: ", firstByte)
        print("Data received in Debug mode: ", receivedData)
    
    opcoderecvd, lengthrecvd = response.decode_first_byte(receivedData)
    if opcoderecvd == response.ResponseType.ERR_UNKNOWN_REQUEST:
        print("Unknown request")


def bye():
    clientSocket.close()
    print("Session is terminated")
    sys.exit()


while True:
    command = input("myftp>")
    command = command.split()
    try:
        if command[0] == 'put':
            if len(command) < 2:
                print("Syntax error: file name required")
            else:
                put(command[1])
        elif command[0] == 'get':
            if len(command) < 2:
                print("Syntax error: file name required")
            else:
                get(command[1])
        elif command[0] == 'change':
            if len(command) < 3:
                print("Syntax error: original and new file names required")
            else:
                change(command[1], command[2])
        elif command[0] == 'help':
            help()
        elif command[0] == 'bye':
            bye()
        else:
            print('Unknown command, try "help".')
    except ValueError as e:
        print("An error occurred while executing the command:", e)