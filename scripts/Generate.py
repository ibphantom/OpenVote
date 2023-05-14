from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import csv
import subprocess

# Generate three public/private key pairs
keys = []
for i in range(1, 4):
    key = RSA.generate(4096)
    keys.append(key)
    with open(f"decryptkey-{i}.pem", "wb") as f:
        f.write(key.export_key(format="PEM"))

# Load the CSV file to encrypt
with open("/VOTE/FINAL.csv", "r") as f:
    reader = csv.reader(f)
    data = list(reader)

# Encrypt each row of the CSV file with each of the public keys
encrypted_data = []
for row in data:
    encrypted_row = []
    for key in keys:
        cipher = PKCS1_OAEP.new(key)
        encrypted_value = cipher.encrypt(str(row).encode())
        encrypted_row.append(encrypted_value)
    encrypted_data.append(encrypted_row)

# Save the encrypted data to a new file
with open("/VOTE/encrypted.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(encrypted_data)

subprocess.call(["python3", "/VOTE/vote.py"])
