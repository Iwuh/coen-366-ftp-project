import sys
import os
import unittest

# Need to add parent directory to search path so that we can include modules under test
sys.path.append(os.path.join(sys.path[0], '..'))
import response

class TestResponseMethods(unittest.TestCase):
    def test_decode_first_byte(self):
        # Equivalent to 00111001
        b = b'\x39'

        type, length = response.decode_first_byte(b)

        self.assertEqual(type, response.ResponseType.GET)
        self.assertEqual(length, 25)

    def test_encode_put_change_successful(self):
        # Message returned should be 00000000
        expected = b'\x00'

        msg = response.encode_put_change_successful()

        self.assertEqual(expected, msg)

    def test_encode_get_successful(self):
        fileName = "test.txt"
        fileSize = 30000
        # Opcode: 0b001
        # Filename length: 0b01000 (8)
        # Filename: test.txt
        # Filesize: 0x00007530 
        expected = b'\x28test.txt\x00\x00\x75\x30'

        msg = response.encode_get_successful(fileName, fileSize)

        self.assertEqual(expected, msg)

    def test_encode_get_not_found(self):
        # Message should be 01000000
        expected = b'\x40'

        msg = response.encode_get_not_found()

        self.assertEqual(expected, msg)
        
if __name__ == "__main__":
    unittest.main()