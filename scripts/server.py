#!/usr/bin/env python3
"""
Server-side vote aggregator.

Changes
- Fixed syntax errors and hostname handling.
- Unified remote file paths and added safe appends with header control.
- Parametrized authentication with either password or private key.
- No destructive deletions of client files.
"""

from scapy.all import ARP, Ether, srp  # Requires scapy and appropriate privileges
import paramiko
import socket
import csv
from pathlib import Path
from typing import List, Dict, Optional

OPENVOTE_ROOT = Path("/OpenVote")
AGGREGATE_CSV = OPENVOTE_ROOT / "VOTES.csv"     # Aggregated hashes from clients
CLIENT_LIST = OPENVOTE_ROOT / "client_info.txt" # Scan results

# Network scan range
SCAN_CIDR = "172.16.0.0/24"

# Remote file location on clients
REMOTE_FINAL = "/OpenVote/FINAL.csv"

# Auth configuration
SSH_USERNAME = "openvote"  # Provision this user out-of-band with key-based auth
SSH_PASSWORD: Optional[str] = None  # Use only if you must. Prefer keys.
SSH_KEY_PATH: Optional[Path] = None  # Example: Path("/home/server/.ssh/id_ed25519")


def scan(ip_cidr: str) -> List[Dict[str, str]]:
    arp = ARP(pdst=ip_cidr)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]

    clients: List[Dict[str, str]] = []
    for _, received in result:
        ip = received.psrc
        mac = received.hwsrc
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except Exception:
            hostname = ""
        clients.append({"ip": ip, "mac": mac, "hostname": hostname})
    return clients


def save_clients(clients: List[Dict[str, str]]) -> None:
    OPENVOTE_ROOT.mkdir(parents=True, exist_ok=True)
    with CLIENT_LIST.open("w", encoding="utf-8") as f:
        f.write("IP\tMAC Address\tHostname\n")
        for c in clients:
            f.write(f"{c['ip']}\t{c['mac']}\t{c['hostname']}\n")


def sftp_get_file(ip: str, username: str, remote_path: str, local_tmp: Path) -> bool:
    try:
        transport = paramiko.Transport((ip, 22))
        if SSH_KEY_PATH:
            pkey = paramiko.Ed25519Key.from_private_key_file(str(SSH_KEY_PATH)) if SSH_KEY_PATH.suffix == "" else paramiko.RSAKey.from_private_key_file(str(SSH_KEY_PATH))
            transport.connect(username=username, pkey=pkey)
        elif SSH_PASSWORD:
            transport.connect(username=username, password=SSH_PASSWORD)
        else:
            print(f"[{ip}] No auth configured.")
            return False

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remote_path, str(local_tmp))
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print(f"[{ip}] SFTP error: {e}")
        return False


def append_hashes_to_aggregate(src_csv: Path) -> int:
    if not src_csv.exists():
        return 0

    # Ensure aggregate header
    if not AGGREGATE_CSV.exists():
        with AGGREGATE_CSV.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["hash"])

    # Load existing to deduplicate
    existing = set()
    with AGGREGATE_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if "hash" in reader.fieldnames:
            for row in reader:
                h = row.get("hash", "").strip()
                if h:
                    existing.add(h)

    added = 0
    with src_csv.open("r", encoding="utf-8", newline="") as sf, \
         AGGREGATE_CSV.open("a", encoding="utf-8", newline="") as df:
        sreader = csv.DictReader(sf)
        dwriter = csv.writer(df)
        # Backward compatibility if client wrote plain rows
        if not sreader.fieldnames or "hash" not in sreader.fieldnames:
            sf.seek(0)
            raw = csv.reader(sf)
            for row in raw:
                if not row:
                    continue
                h = row[0].strip()
                if h and h not in existing:
                    dwriter.writerow([h])
                    existing.add(h)
                    added += 1
        else:
            for row in sreader:
                h = row.get("hash", "").strip()
                if h and h not in existing:
                    dwriter.writerow([h])
                    existing.add(h)
                    added += 1
    return added


def main() -> int:
    OPENVOTE_ROOT.mkdir(parents=True, exist_ok=True)

    print(f"Scanning {SCAN_CIDR} for clients.")
    clients = scan(SCAN_CIDR)
    print(f"Found {len(clients)} hosts.")
    save_clients(clients)
    print(f"Results saved to {CLIENT_LIST}")

    total_added = 0
    for c in clients:
        hostname = c.get("hostname") or ""
        ip = c["ip"]
        # Filter by naming convention if you use one. Otherwise harvest all reachable.
        # Example: only hosts containing 'openvote'
        # if "openvote" not in hostname.lower():
        #     continue

        tmp_file = OPENVOTE_ROOT / f"{ip.replace('.', '_')}_FINAL.tmp.csv"
        ok = sftp_get_file(ip, SSH_USERNAME, REMOTE_FINAL, tmp_file)
        if not ok:
            continue
        added = append_hashes_to_aggregate(tmp_file)
        tmp_file.unlink(missing_ok=True)
        if added > 0:
            print(f"[{ip}] Imported {added} new hashes.")
            total_added += added

    print(f"Aggregation complete. New hashes added: {total_added}. Output: {AGGREGATE_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
