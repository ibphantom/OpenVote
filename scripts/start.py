import subprocess
import sys
import os
import socket
import uuid

while True:
    try:
        device_type = input("Is this device a server or a client? ")
        break
    except EOFError:
        print("Error: End of input reached unexpectedly. Please try again.")

# Create a cron job to start vote.py on boot
cron_job = f'@reboot python3 /vote.py >/dev/null 2>&1\n'

# Open the crontab file for editing and write the cron job
with open('/etc/crontab', 'a') as file:
    file.write(cron_job)

if device_type.lower() == "server":
    print("This device is a server.")
    subprocess.run(["python3", "sftp.py"])
elif device_type.lower() == "client":
    print("This device is a client.")
    # Generate a random hostname if one doesn't already exist
    current_hostname = socket.gethostname()
    if current_hostname.startswith("localhost"):
        new_hostname = f"client-{str(uuid.uuid4())[:8]}"
        subprocess.run(["sudo", "hostnamectl", "set-hostname", new_hostname])
    subprocess.run(["python3", "hostname.py"])
else:
    print("Invalid input. Please enter either 'server' or 'client'.")

input("Press Enter to exit...")
