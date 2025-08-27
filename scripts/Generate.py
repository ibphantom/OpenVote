#!/usr/bin/env python3
"""
Encrypt FINAL.csv rows using RSA public keys.

Changes
- Correct RSA usage: encrypt with public keys, keep private keys offline.
- Base64 encodes ciphertexts for CSV storage.
- Generates keypairs if missing, writes to ./keys/.
- Reads from /OpenVote/FINAL.csv and writes /OpenVote/encrypted.csv.
- Assumes rows contain a single 'hash' column.
"""

import csv
import os
import base64
from pathlib import Path
from typing import List

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

OPENVOTE_ROOT = Path("/OpenVote")
FINAL_CSV = OPENVOTE_ROOT / "FINAL.csv"
ENCRYPTED_CSV = OPENVOTE_ROOT / "encrypted.csv"
KEYS_DIR = Path("./keys")
KEY_COUNT = 3  # number of independent recipients

KEYS_DIR.mkdir(parents=True, exist_ok=True)


def ensure_keys() -> List[RSA.RsaKey]:
    keys: List[RSA.RsaKey] = []
    for i in range(1, KEY_COUNT + 1):
        priv_path = KEYS_DIR / f"decryptkey-{i}.pem"
        pub_path = KEYS_DIR / f"publickey-{i}.pem"
        if priv_path.exists() and pub_path.exists():
            key = RSA.import_key(priv_path.read_bytes())
        else:
            key = RSA.generate(4096)
            priv_path.write_bytes(key.export_key("PEM"))
            pub_path.write_bytes(key.publickey().export_key("PEM"))
        keys.append(key)
    return keys


def load_public_keys(keys: List[RSA.RsaKey]) -> List[RSA.RsaKey]:
    return [k.publickey() for k in keys]


def read_hashes() -> List[str]:
    if not FINAL_CSV.exists():
        return []
    hashes: List[str] = []
    with FINAL_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames and "hash" in reader.fieldnames:
            for row in reader:
                h = row.get("hash", "").strip()
                if h:
                    hashes.append(h)
        else:
            f.seek(0)
            raw = csv.reader(f)
            for row in raw:
                if row and row[0].strip():
                    hashes.append(row[0].strip())
    return hashes


def encrypt_rows(pub_keys: List[RSA.RsaKey], hashes: List[str]) -> List[List[str]]:
    """
    Returns a list of rows where each row contains the ciphertext for each recipient.
    Ciphertext is base64-encoded for CSV compatibility.
    """
    encrypted_rows: List[List[str]] = []
    ciphers = [PKCS1_OAEP.new(k) for k in pub_keys]
    for h in hashes:
        row_ct: List[str] = []
        payload = h.encode("utf-8")
        for c in ciphers:
            ct = c.encrypt(payload)
            row_ct.append(base64.b64encode(ct).decode("ascii"))
        encrypted_rows.append(row_ct)
    return encrypted_rows


def write_encrypted(encrypted_rows: List[List[str]]) -> None:
    headers = [f"key{i}" for i in range(1, len(encrypted_rows[0]) + 1)] if encrypted_rows else []
    with ENCRYPTED_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        writer.writerows(encrypted_rows)


def main() -> int:
    keys = ensure_keys()
    pub_keys = load_public_keys(keys)
    hashes = read_hashes()
    if not hashes:
        print(f"No hashes found in {FINAL_CSV}. Nothing to encrypt.")
        return 0
    encrypted_rows = encrypt_rows(pub_keys, hashes)
    write_encrypted(encrypted_rows)
    print(f"Encrypted {len(encrypted_rows)} rows to {ENCRYPTED_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
