from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import csv

# Generate key pairs
keys = []
for i in range(1, 4):
    key = RSA.generate(4096)
    keys.append(key)
    with open(f"decryptkey-{i}.pem", "wb") as f:
        f.write(key.export_key(format="PEM"))

# Load votes
with open("/OpenVote/FINAL.csv", "r") as f:
    reader = csv.reader(f)
    data = list(reader)

# Encrypt votes
encrypted_data = []
for row in data:
    encrypted_row = []
    for key in keys:
        cipher = PKCS1_OAEP.new(key.publickey())
        encrypted_row.append(cipher.encrypt(",".join(row).encode()))
    encrypted_data.append(encrypted_row)

# Save encrypted data
with open("/OpenVote/encrypted.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(encrypted_data)
