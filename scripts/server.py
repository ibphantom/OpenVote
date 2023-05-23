import socket
import time
import paramiko

def get_client_info():
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    return host, ip

def write_client_info_to_file(filename, client_info):
    with open(filename, 'a') as file:
        file.write(f'{client_info[0]} {client_info[1]}\n')

def read_client_info_from_file(filename):
    clients = []
    with open(filename, 'r') as file:
        for line in file:
            client = line.strip().split()
            if len(client) == 2:
                clients.append(client)
    return clients

def connect_and_sftp_to_clients(clients):
    server_host = 'SERVER_HOST'  # Replace with the server's IP or hostname
    server_port = 22  # Replace with the server's SSH port
    username = 'YOUR_USERNAME'  # Replace with your SSH username
    private_key_path = 'PATH_TO_PRIVATE_KEY'  # Replace with the path to your private key file

    for client in clients:
        client_host = client[1]  # Assuming the IP address is stored in the second element
        try:
            # Connect to the client using SFTP
            transport = paramiko.Transport((client_host, server_port))
            private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
            transport.connect(username=username, pkey=private_key)
            sftp = transport.open_sftp()
            
            # Perform SFTP operations with the client
            # Add your code here to interact with the client's SFTP server
            
            sftp.close()
            transport.close()
            
            print(f"Connected and performed SFTP operations with {client_host}")
        except paramiko.AuthenticationException:
            print(f"Authentication failed for {client_host}")
        except paramiko.SSHException as e:
            print(f"SSH connection failed for {client_host}: {str(e)}")
        except Exception as e:
            print(f"Error connecting to {client_host}: {str(e)}")

def main():
    filename = 'client_info.txt'  # Change this to your desired filename
    clients = read_client_info_from_file(filename)
    current_time = time.strftime('%H:%M')  # Get the current time in HH:MM format

    # Set the desired time to initiate the SFTP connections (in HH:MM format)
    target_time = '12:00'

    if current_time == target_time:
        connect_and_sftp_to_clients(clients)

if __name__ == '__main__':
    main()
