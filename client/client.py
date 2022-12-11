#Ben Hitterman (40174961)
#Purpose: Client of program that sends a message to the server and receives a response

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

        with open(fileName, 'rb') as file:
            fileData = file.read()
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
        fileData = clientSocket.recv(fileSize) #getting file data

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
    request = input("myftp>")
    request = request.split()
    if request[0] == 'put':
        put(request[1])
    elif request[0] == 'get':
        get(request[1])
    elif request[0] == 'change':
        change(request[1], request[2])
    elif request[0] == 'help':
        help()
    elif request[0] == 'bye':
        bye()
    else:
        unknownRequest(request[0])