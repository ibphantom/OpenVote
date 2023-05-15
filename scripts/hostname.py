import subprocess
import requests
import random
import string

# Get a random word from the Wordnik API
response = requests.get("https://api.wordnik.com/v4/words.json/randomWord?api_key=YOUR_API_KEY")
if response.status_code != 200:
    print("Error getting random word")
    exit()
random_word = response.json()["word"]

# Generate a random string of length 8 for suffix
suffix = ''.join(random.choices(string.ascii_lowercase, k=8))

# Concatenate the hostname prefix and suffix
new_hostname = f"VoterMachine-{random_word}-{suffix}"

# Rename the hostname
subprocess.run(["hostnamectl", "set-hostname", new_hostname])

# Reboot the machine
subprocess.run(["reboot"])
