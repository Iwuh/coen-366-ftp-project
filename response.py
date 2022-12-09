import enum
from typing import Tuple

class ResponseType(enum.Enum):
    PUT_CHANGE          = 0b000
    GET                 = 0b001
    ERR_NOT_FOUND       = 0b010
    ERR_UNKNOWN_REQUEST = 0b011
    ERR_CHANGE_FAILED   = 0b101
    HELP                = 0b110

def decode_first_byte(b: bytes) -> Tuple[ResponseType, int]:
    '''
    Takes a single byte and returns a 2-tuple containing the decoded opcode and length bits.
    The opcode is an instance of RequestType.
    The length is an integer.
    Throws ValueError if the argument is not 1 byte large or the opcode is unknown.
    '''
    if (len(b) != 1):
        raise ValueError('Input is not 1 byte')
    i = int.from_bytes(b, 'big')
    o = ResponseType(i >> 5)
    l = i & 0b00011111
    return (o, l)

def encode_put_change_successful() -> bytes:
    '''
    Returns a bytes object representing a successful put or change operation.
    '''
    return (ResponseType.PUT_CHANGE.value << 5).to_bytes(1, 'big')

def encode_get_successful(fileName: str, fileSize: int) -> bytes:
    '''
    Returns a bytes object representing a successful get operation.
    fileName is the name of the file that was requested by the user.
    fileSize is the size of the file that will be sent to the user.
    Once this message is sent, it should be immediately followed by the file bytes.
    '''
    b1 = (ResponseType.GET.value << 5) + len(fileName)
    return b1.to_bytes(1, 'big') + fileName.encode() + fileSize.to_bytes(4, 'big')

def encode_get_not_found() -> bytes:
    '''
    Returns a bytes object representing a failed get operation.
    '''
    return (ResponseType.ERR_NOT_FOUND.value << 5).to_bytes(1, 'big')

def encode_change_failed() -> bytes:
    '''
    Returns a bytes object representing a failed change operation.
    '''
    return (ResponseType.ERR_CHANGE_FAILED.value << 5).to_bytes(1, 'big')

def encode_help_response() -> bytes:
    '''
    Returns a bytes object representing a help message.
    '''
    helpBytes = ('Cmds: put get change help bye').encode()
    b1 = (ResponseType.HELP.value << 5) + len(helpBytes)
    return b1.to_bytes(1, 'big') + helpBytes

def encode_unknown_request_response() -> bytes:
    '''
    Returns a bytes object representing an unknown command opcode.
    '''
    return (ResponseType.ERR_UNKNOWN_REQUEST.value << 5).to_bytes(1, 'big')