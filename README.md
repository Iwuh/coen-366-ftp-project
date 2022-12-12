# COEN 366 Term Project
Basic FTP server for Communication Networks and Protocols

# Demonstration Procedure
1. Open a terminal in `/server`.
2. Launch the server with:
    * `python server.py` (Windows, non-debug)
    * `python server.py 1` (Windows, debug)
    * `python3 server.py` (Linux, non-debug)
    * `python3 server.py 1` (Linux, debug)
3. Launch the client with:
    * `python client.py localhost 12000` (Windows, non-debug)
    * `python client.py localhost 12000 1` (Windows, debug)
    * `python3 client.py localhost 12000` (Linux, non-debug)
    * `python3 client.py localhost 12000 1` (Linux, debug)
4. Create a file (`test.txt`) in `/client` with arbitrary contents.
5. Obtain a list of commands with `help`.
6. Send the file to the server with `put test.txt`.
7. Rename the file with `change test.txt test2.txt`.
8. Download the new file with `get test.txt`.
9. Disconnect from the server with `bye`.

The server will continue running once the client disconnects and can be reconnected to. Only one client will be accepted at a time. Various incorrect commands can be tested to verify error handling.

# Unit Testing
Unit tests for the `request` and `response` modules are provided in the `/tests` directory. These tests use the built-in unit testing library and can be run by simply running the script.