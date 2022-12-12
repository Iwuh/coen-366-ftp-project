import enum
from typing import Tuple

class RequestType(enum.Enum):
    PUT     = 0b000
    GET     = 0b001
    CHANGE  = 0b010
    HELP    = 0b011

def decode_first_byte(b: bytes) -> Tuple[RequestType, int]:
    '''
    Takes a single byte and returns a 2-tuple containing the decoded opcode and length bits.
    The opcode is an instance of RequestType.
    The length is an integer.
    Throws ValueError if the argument is not 1 byte large or the opcode is unknown.
    '''
    if (len(b) != 1):
        raise ValueError('Input is not 1 byte')
    i = int.from_bytes(b, 'big')
    o = RequestType(i >> 5)
    l = i & 0b00011111
    return (o, l)

def encode_put(fileName: str, fileSize: int) -> bytes:
    '''
    Encodes a request to put a file with a specified name and size.
    Throws ValueError if the name is longer than 31 characters.
    '''
    if len(fileName) > 31:
        raise ValueError('File name cannot exceed 31 characters')
    firstByte = (RequestType.PUT.value << 5) + len(fileName)
    secondByte = fileName
    thirdByte = fileSize
    return firstByte.to_bytes(1,'big') + secondByte.encode() + thirdByte.to_bytes(4,'big')

def encode_get(fileName: str) -> bytes:
    '''
    Encodes a request to get a file with a specified name.
    Throws ValueError if the name is longer than 31 characters.
    '''
    if len(fileName) > 31:
        raise ValueError('File name cannot exceed 31 characters')
    firstByte = (RequestType.GET.value << 5) + len(fileName)
    secondByte = fileName
    return firstByte.to_bytes(1,'big') + secondByte.encode()

def encode_change(oldFileName: str, newFileName: str) -> bytes:
    '''
    Encodes a request to rename a file on the remote server.
    Throws ValueError if either name is longer than 31 characters.
    '''
    if len(oldFileName) > 31 or len(newFileName) > 31:
        raise ValueError('File name cannot exceed 31 characters')
    firstByte = (RequestType.CHANGE.value << 5) + len(oldFileName)
    secondByte = oldFileName
    thirdByte = len(newFileName)
    fourthByte = newFileName
    return firstByte.to_bytes(1,'big') + secondByte.encode() + thirdByte.to_bytes(1,'big') + fourthByte.encode()

def encode_help() -> bytes:
    '''
    Encodes a request for the list of valid commands from the server.
    '''
    firstByte = RequestType.HELP.value << 5
    return firstByte.to_bytes(1,'big')