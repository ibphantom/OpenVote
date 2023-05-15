import subprocess
import random_word

# Generate a random word
random_word = random_word.RandomWords().get_random_word()

# Check if a random word is generated
if random_word:
    # Concatenate the hostname prefix and the random word
    new_hostname = "VoterMachine-" + random_word

    # Rename the hostname
    subprocess.run(["hostnamectl", "set-hostname", new_hostname])

    # Reboot the machine
    subprocess.run(["reboot"])
else:
    print("Failed to generate a random word.")
