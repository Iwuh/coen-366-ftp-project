# COEN 366 Term Project
Basic FTP server for Communication Networks and Protocols

# Demonstration Procedure
1. Open a terminal in `/server`.
2. Launch the server with:
    * `python server.py` (Windows, non-debug)
    * `python server.py 1` (Windows, debug)
    * `python3 server.py` (Linux, non-debug)
    * `python3 server.py 1` (Linux, debug)
3. Open a new terminal in `/client`.
4. Create a file (`test.txt`) in `/client` with arbitrary contents.
5. Launch the client with:
    * `python client.py localhost 12000` (Windows, non-debug)
    * `python client.py localhost 12000 1` (Windows, debug)
    * `python3 client.py localhost 12000` (Linux, non-debug)
    * `python3 client.py localhost 12000 1` (Linux, debug)
6. Obtain a list of commands with `help`.
7. Send the file to the server with `put test.txt`.
8. Rename the file with `change test.txt test2.txt`.
9. Download the new file with `get test2.txt`.
10. Disconnect from the server with `bye`.

The server will continue running once the client disconnects and can be reconnected to by relaunching the client script. Only one client will be accepted at a time. 

Various incorrect commands can be tested to verify error handling:
   * Leaving out required arguments
   * Using too-long file names (longer than 31 characters)
   * Requesting files that don't exist
   * Renaming files that don't exist
   * etc...

# Unit Testing
Unit tests for the `request` and `response` modules are provided in the `/tests` directory. These tests use the built-in unit testing library and can be run by simply running the script.
