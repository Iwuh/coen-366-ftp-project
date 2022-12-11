import sys
import os
import unittest

# Add parent directory to import list so we can include request and response modules
sys.path.append(os.path.join(sys.path[0], '..'))
import request

class TestRequestMethods(unittest.TestCase):
    def test_decode_first_byte(self):
        # Equivalent to 01011001
        b = b'\x59'

        type, length = request.decode_first_byte(b)

        self.assertEqual(type, request.RequestType.CHANGE)
        self.assertEqual(length, 25)

    def test_encode_put(self):
        fileName = "test.txt"
        fileSize = 30000
        # Opcode: 0b000
        # Filename length: 0b01000 (8)
        # Filename: test.txt
        # Filesize: 0x00007530 
        expected = b'\x08test.txt\x00\x00\x75\x30'

        msg = request.encode_put(fileName, fileSize)

        self.assertEqual(expected, msg)
 
    def test_encode_get(self):
        fileName = "test.txt"
        # Opcode: 0b001
        # Filename length: 0b01000 (8)
        # Filename: test.txt
        expected = b'\x28test.txt'

        msg = request.encode_get(fileName)

        self.assertEqual(expected, msg)

    def test_encode_change(self):
        oldFileName = "test.txt"
        newFileName = "testttt.txt"
        # Opcode: 0b010
        # Old filename length: 0b01000 (8)
        # Old filename: test.txt
        # New filename length: 0b00001011 (11)
        # New filename: testttt.txt

        expected = b'\x48test.txt\x0btestttt.txt'

        msg = request.encode_change(oldFileName, newFileName)

        self.assertEqual(expected, msg)

    def test_encode_help(self):
        # 0b01100000
        expected = b'\x60'

        msg = request.encode_help()

        self.assertEqual(expected, msg)

if __name__ == "__main__":
    unittest.main()