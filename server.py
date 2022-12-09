from socket import *

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('localhost', 12000))
    serverSocket.listen(1)
    print('Server started')
    while True:
        connectionSocket, addr = serverSocket.accept()
        while True:
            pass

if __name__ == "__main__":
    main()