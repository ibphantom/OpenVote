import os
import socket
from scapy.all import ARP, Ether, srp
import paramiko

def scan(ip):
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    clients = []

    for sent, received in result:
        try:
            hostname = socket.gethostbyaddr(received.psrc)[0]
        except socket.herror:
            hostname = ''
        clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'hostname': hostname})

    return clients


def sftp_transfer(ip, username, password, files):
    transport = paramiko.Transport((ip, 22))
    transport.connect(username=username, password=password)
    sftp = transport.open_sftp()
    
    for file in files:
        remote_path = file
        local_path = os.path.join(os.getcwd(), os.path.basename(file))
        sftp.get(remote_path, local_path)
    
    sftp.close()
    transport.close()


subnet = "172.16.0.254/24"
target_files = ["FINAL.csv", "count.csv"]

# Scan the subnet and retrieve a list of clients
clients = scan(subnet)

# Iterate over the discovered clients and perform SFTP
for client in clients:
    ip_address = client['ip']
    username = "zach"
    password = "123456"
    
    sftp_transfer(ip_address, username, password, target_files)
