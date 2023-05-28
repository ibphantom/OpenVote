from scapy.all import ARP, Ether, srp
import paramiko
import socket
import csv
import os

def scan(ip):
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    clients = []

    for sent, received in result:
        try:
            hostname = socket.gethostbyaddr(received.psrc)[0]
        except socket.herror:  # unable to resolve
            hostname = ''
        
        clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'hostname': hostname})

    return clients


def save_to_file(clients):
    with open('client_info.txt', 'w') as file:
        file.write('IP\t\t\tMAC Address\t\tHostname\n')
        for client in clients:
            file.write(f"{client['ip']}\t\t{client['mac']}\t\t{client['hostname']}\n")


def sftp_get_file(ip, username, password, remote_file_path, local_file_path):
    try:
        transport = paramiko.Transport((ip, 22))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remote_file_path, local_file_path)
        print(f"Downloaded {remote_file_path} to {local_file_path}.")

        # Read the content of the downloaded file and append it to VOTES.csv
        with open(local_file_path, 'r') as source_file:
            reader = csv.reader(source_file)
            data = list(reader)
            print(f"Read {len(data)} rows from {local_file_path}.")
            with open('VOTES.csv', 'a') as destination_file:
                writer = csv.writer(destination_file)
                for row in data:
                    writer.writerow(row + [ip])
                print(f"Appended data to VOTES.csv.")

        sftp.close()
        transport.close()

        print(f"Downloaded and appended {remote_file_path} from {ip}")
    except Exception as e:
        print(f"Failed to download and append {remote_file_path} from {ip}. Error: {str(e)}")

if __name__ == "__main__":
    ip_address = "172.16.0.254/24"  # adjust this to fit your network
    username = "zach"  # fill in
    password = "123456"  # fill in

    # Delete FINAL.csv
    if os.path.exists("FINAL.csv"):
        os.remove("FINAL.csv")
        print("FINAL.csv deleted.")

    # Delete start.py
    if os.path.exists("start.py"):
        os.remove("start.py")
        print("start.py deleted.")

    # Delete vote.py
    if os.path.exists("vote.py"):
        os.remove("vote.py")
        print("vote.py deleted.")

    # Delete client_info.txt
    if os.path.exists("client_info.txt"):
        os.remove("client_info.txt")
        print("client_info.txt deleted.")

    print(f"Scanning {ip_address}...")
    clients = scan(ip_address)
    print(f"Found {len(clients)} hosts.")
    save_to_file(clients)
    print("Results saved to client_info.txt")

    for client in clients:
        if 'openvote' in client['hostname']:
            print(f"Found openvote host: {client['hostname']}")
            sftp_get_file(client['ip'], username, password, '/VOTE/FINAL.csv', f"{client['hostname']}_FINAL.csv")
