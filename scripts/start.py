import subprocess

try:
    device_type = input("Is this device a server or a client? ")
except EOFError:
    print("Error: End of input reached unexpectedly.")
    exit(1)

if device_type.lower() == "server":
    print("This device is a server.")
    subprocess.run(["python", "sftp.py"])
elif device_type.lower() == "client":
    print("This device is a client.")
    subprocess.run(["python", "vote.py"])
else:
    print("Invalid input. Please enter either 'server' or 'client'.")

input("Press Enter to exit...")
