from scapy.all import ARP, Ether, srp
import socket

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


if __name__ == "__main__":
    ip_address = "192.168.1.1/24"  # adjust this to fit your network
    print(f"Scanning {ip_address}...")
    clients = scan(ip_address)
    print(f"Found {len(clients)} hosts.")
    save_to_file(clients)
    print("Results saved to client_info.txt")
