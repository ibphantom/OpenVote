import os.path
import paramiko
import getpass

def Update():
    # Install packages
    os.system('apt-get install -y openssh-server ufw')

    #Create user
    #os.system('useradd zach -m -s /bin/bash')
    #os.system('echo "zach:123456" | chpasswd')

    # Create /run/sshd directory
    os.system('mkdir -p /run/sshd')

    # Set permissions for /run/sshd
    os.system('chmod 0755 /run/sshd')

    # Start sshd daemon
    os.system('/usr/sbin/sshd -D')

# Define local and remote file paths
local_file_path = 'C:/file.txt'
remote_file_path = '/mnt/user/UnraidNAS/ptest/contact.txt'

# Prompt the user for connection parameters
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")
port = 22

# List of hostnames
hostnames = ["172.16.0.2", "172.16.0.3", "172.16.0.4"]  # replace with your hostnames

for hostname in hostnames:
    # Create a new SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the server using SSH
    ssh.connect(hostname=hostname, username=username, password=password, port=port)

    # Open an SFTP session over the existing SSH connection
    sftp = ssh.open_sftp()

    print("Connected to {}".format(hostname))

    # Transfer the file from remote to local
    sftp.get(remote_file_path, local_file_path)  # replacing sftp.put with sftp.get

    # Close the SFTP session and the SSH connection
    sftp.close()
    ssh.close()

    print("File transferred successfully from {}".format(hostname))
