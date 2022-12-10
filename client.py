#Ben Hitterman (40174961)
#Purpose: Client of program that sends a message to the server and receives a response

import os.path
from socket import *
import sys
import response

#server linking to client format: python3file ipAddress portNumber debugMode

#retrive server ip
serverIpAddress = sys.argv[1]
#retrive server port
serverPort = int(sys.argv[2])
#for Debug Mode
if (sys.argv[3] == '0'):
    debug = False
else:
    debug = True


clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIpAddress, serverPort))
print('Session has been established')


def put(fileName):
    if os.path.isfile(fileName):
        firstByte = (0b000 << 5) + len(fileName)
        secondByte = fileName
        thirdByte = os.path.getsize(fileName)
        request = firstByte.to_bytes(1,'big') + secondByte.encode() + thirdByte.to_bytes(4,'big')
        clientSocket.send(request)

        with open(fileName, 'rb') as file:
            fileData = file.read()
            clientSocket.send(fileData)


        dataReceived = clientSocket.recv(1).decode()

        if debug:
            print("Request sent in Debug mode: " + request)
            print("Data sent in Debug mode: " + fileData)
            print("Data received in Debug mode: " + dataReceived)


        opcoderecvd, lengthrecvd = response.decode_first_byte(dataReceived)
        if opcoderecvd == response.ResponseType.PUT_CHANGE:
            print(fileName + " has been uploaded successfully")
        else:
            print(fileName + " not sent successfully")

    else:
        print(fileName + " does not exist")


def get(fileName):
    firstByte = (0b001 << 5) + len(fileName)
    secondByte = fileName
    request = firstByte.to_bytes(1,'big') + secondByte.encode()
    clientSocket.send(request)

    dataReceived = clientSocket.recv(1).decode()

    if debug:
        print("Request sent in Debug mode: " + request)
        print("Data received in Debug mode: " + dataReceived)


    opcoderecvd, lengthrecvd = response.decode_first_byte(dataReceived)
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
            print("File data received in Debug mode: " + fileData)

        print(fileName + " has been downloaded successfully")
    
    elif opcoderecvd == response.ResponseType.ERR_NOT_FOUND:
        print(fileName + " not found")



    

def change(oldFileName, newFileName):
    firstByte = (0b010 << 5) + len(oldFileName)
    secondByte = oldFileName
    thirdByte = os.path.getsize(newFileName)
    fourthByte = newFileName
    request = firstByte.to_bytes(1,'big') + secondByte.encode() + thirdByte.to_bytes(4,'big') + fourthByte.encode()
    clientSocket.send(request)

    dataReceived = clientSocket.recv(1).decode()

    if debug:
        print("Request sent in Debug mode: " + request)
        print("Data received in Debug mode: " + dataReceived)


    opcoderecvd, lengthrecvd = response.decode_first_byte(dataReceived)
    if opcoderecvd == response.ResponseType.PUT_CHANGE:
        print(oldFileName + " has been changed to " + newFileName + " successfully")
    elif opcoderecvd == response.ResponseType.ERR_CHANGE_FAILED:
        print(oldFileName + " not changed successfully")


def help():
    firstByte = 0b01100000
    request = firstByte.to_bytes(1,'big')
    clientSocket.send(request)

    dataReceived = clientSocket.recv(1).decode()

    if debug:
        print("Request sent: " + request)
        print("Data received: " + dataReceived)

    opcoderecvd, lengthrecvd = response.decode_first_byte(dataReceived)
    if opcoderecvd == response.ResponseType.HELP:
        print(clientSocket.recv(lengthrecvd).decode()) #printing 5 commands fetched from server
    else:
        print("Help not found")

def unknownRequest(request):
    firstByte = request.encode()
    clientSocket.send(firstByte)


    dataReceived = clientSocket.recv(1).decode()

    if debug:
        print("Request sent in Debug mode: " + firstByte)
        print("Data received in Debug mode: " + dataReceived)
    
    opcoderecvd, lengthrecvd = response.decode_first_byte(dataReceived)
    if opcoderecvd == response.ResponseType.ERR_UNKNOWN_REQUEST:
        print("Unknown request")


def bye():
    clientSocket.close()
    print("Connection closed")
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