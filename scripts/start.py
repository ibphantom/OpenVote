import subprocess
import sys

while True:
    try:
        device_type = input("Is this device a server or a client? ")
        break
    except EOFError:
        print("Error: End of input reached unexpectedly. Please try again.")

if device_type.lower() == "server":
    print("This device is a server.")
    subprocess.run(["python3", "sftp.py"])
elif device_type.lower() == "client":
    print("This device is a client.")
    subprocess.run(["python3", "hostname.py"])
else:
    print("Invalid input. Please enter either 'server' or 'client'.")

input("Press Enter to exit...")
