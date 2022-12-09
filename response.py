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