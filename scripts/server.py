import os.path
import paramiko



while True:
        # Install packages
        os.system('apt-get install -y openssh-server ufw')
        pip install paramiko
        #Create user
        os.system('useradd zach -m -s /bin/bash')
        os.system('echo "zach:123456" | chpasswd')

        # Create /run/sshd directory
        os.system('mkdir -p /run/sshd')

        # Set permissions for /run/sshd
        os.system('chmod 0755 /run/sshd')

        # Start sshd daemon
        os.system('/usr/sbin/sshd -D')


# Define connection parameters
hostname = '172.16.0.2'
username = ''
password = ''
port = 22

# Define local and remote file paths
local_file_path = 'C:/file.txt'
remote_file_path = '/mnt/user/UnraidNAS/ptest/contact.txt'

# Create a new SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the server using SSH
ssh.connect(hostname=hostname, username=username, password=password, port=port)

# Open an SFTP session over the existing SSH connection
sftp = ssh.open_sftp()

print("Connected to {}".format(hostname))

# Transfer the file from local to remote
sftp.put(local_file_path, remote_file_path)

# Close the SFTP session and the SSH connection
sftp.close()
ssh.close()

print("File transferred successfully")
