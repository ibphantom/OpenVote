import os.path
import paramiko
import getpass

def check_hosts(hostnames, username, password, port):
    for host in hostnames:
        response = os.system("ping -c 1 " + host)
        if response == 0:
            print(host, 'is up!')
        else:
            print(host, 'is down!')

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=username, password=password, port=port)
            print("SSH connection successful to ", host)
            ssh.close()
        except Exception as e:
            print("Failed to connect via SSH to ", host, "due to: ", e)

def Update():
    # Your existing code here

# Define local and remote file paths
local_file_path = 'C:/file.txt'
remote_file_path = '/mnt/user/UnraidNAS/ptest/contact.txt'

# Prompt the user for connection parameters
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")
port = 22

# Ask for a list of hostnames
hosts_input = input("Enter a list of hostnames separated by commas: ")
hostnames = [host.strip() for host in hosts_input.split(',')]

# Checking hosts before starting the main script
check_hosts(hostnames, username, password, port)

for hostname in hostnames:
    # Your file transfer code here
    # rest of your code here
