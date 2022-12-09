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

def encode_put(filename: str, filesize: int) -> bytes:

    # Get opcode and filename length
    o = RequestType.PUT.value
    l = len(filename)
    if l > 31:
        raise ValueError('Filename must be 31 characters or less')

    # Create first byte, filename bytes, filesize bytes
    b1 = ((o << 5) + l).to_bytes(1, 'big')
    filename_bytes = filename.encode()
    filesize_bytes = filesize.to_bytes(4, 'big')
    # Concatenate and return
    return b1 + filename_bytes + filesize_bytes
