from scapy.all import ARP, Ether, srp
import paramiko
import socket
import csv
import os

def scan(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    result = srp(ether/arp, timeout=3, verbose=0)[0]

    clients = []
    for sent, received in result:
        try:
            hostname = socket.gethostbyaddr(received.psrc)[0]
        except socket.herror:
            hostname = ''
        clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'hostname': hostname})
    return clients

def save_to_file(clients):
    with open('client_info.txt', 'w') as file:
        file.write('IP\tMAC Address\tHostname\n')
        for client in clients:
            file.write(f"{client['ip']}\t{client['mac']}\t{client['hostname']}\n")

def sftp_get_file(ip, username, password, remote_file, local_file):
    try:
        transport = paramiko.Transport((ip, 22))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remote_file, local_file)

        with open(local_file, 'r') as source:
            reader = csv.reader(source)
            with open('VOTES.csv', 'a', newline='') as dest:
                writer = csv.writer(dest)
                writer.writerows(reader)

        sftp.close()
        transport.close()
    except Exception as e:
        print(f"Failed to fetch file from {ip}: {e}")

if __name__ == "__main__":
    ip_range = "172.16.0.254/24"
    username = "zach"
    password = "123456"

    for file in ["FINAL.csv", "start.py", "vote.py", "client_info.txt"]:
        if os.path.exists(file):
            os.remove(file)

    print(f"Scanning {ip_range}...")
    clients = scan(ip_range)
    save_to_file(clients)

    for client in clients:
        if 'openvote' in client['hostname']:
            sftp_get_file(client['ip'], username, password, '/OpenVote/FINAL.csv', f"{client['hostname']}_FINAL.csv")
