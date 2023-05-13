from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import csv

# Load the private keys
keys = []
for i in range(1, 4):
    with open(f"decryptkey-{i}.pem", "r") as f:
        key = RSA.import_key(f.read())
        keys.append(key)

# Load the encrypted CSV file
with open("encrypted.csv", "r") as f:
    reader = csv.reader(f)
    encrypted_data = list(reader)

# Decrypt each row of the CSV file with all three private keys
decrypted_data = []
for row in encrypted_data:
    decrypted_row = []
    for i, key in enumerate(keys):
        cipher = PKCS1_OAEP.new(key)
        encrypted_value = eval(row[i])
        decrypted_value = cipher.decrypt(encrypted_value)
        decrypted_row.append(decrypted_value.decode())
    decrypted_data.append(decrypted_row)

# Save the decrypted data to a new file
with open("decrypted.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(decrypted_data)
