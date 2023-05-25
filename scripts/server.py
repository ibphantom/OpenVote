from scapy.all import ARP, Ether, srp
import paramiko
import socket
import csv

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

        # Read the content of the downloaded file and append it to VOTES.CSV
        with open(local_file_path, 'r') as source_file:
            reader = csv.reader(source_file)
            with open('VOTES.CSV', 'a') as destination_file:
                writer = csv.writer(destination_file)
                for row in reader:
                    writer.writerow(row + [ip])

        sftp.close()
        transport.close()

        print(f"Downloaded and appended {remote_file_path} from {ip}")
    except Exception as e:
        print(f"Failed to download and append {remote_file_path} from {ip}. Error: {str(e)}")


if __name__ == "__main__":
    ip_address = "172.16.0.254/24"  # adjust this to fit your network
    username = ""  # fill in
    password = ""  # fill in

    print(f"Scanning {ip_address}...")
    clients = scan(ip_address)
    print(f"Found {len(clients)} hosts.")
    save_to_file(clients)
    print("Results saved to client_info.txt")

    for client in clients:
        if 'openvote' in client['hostname']:
            print(f"Found openvote host: {client['hostname']}")
            sftp_get_file(client['ip'], username, password, '/VOTE/FINAL.CSV', f"{client['hostname']}_FINAL.CSV")
