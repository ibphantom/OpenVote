# Your Python script

import subprocess
import sys
import os
import socket
import uuid
import random

while True:
    try:
        device_type = input("Is this device a server or a client? ")
        break
    except EOFError:
        print("Error: End of input reached unexpectedly. Please try again.")

# Create a script to start vote.py on boot if the device is a client
if device_type.lower() == "client":
    with open('/VOTE/vote', 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('/usr/bin/python3 /OpenVote/vote.py >> /path/to/logfile.log 2>&1\n')
    os.chmod('/VOTE/vote', 0o755)

if device_type.lower() == "server":
    print("This device is a server.")
    subprocess.run(["python3", "server.py"])
elif device_type.lower() == "client":
    print("This device is a client.")
    subprocess.run(["python3", "vote.py"])
else:
    print("Invalid input. Please enter either 'server' or 'client'.")

input("Press Enter to exit...")
