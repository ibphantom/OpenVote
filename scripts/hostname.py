#!/usr/bin/env python3

import os
import random
import subprocess

# List of words to choose from
words = ["apple", "banana", "cherry", "grape", "lemon", "orange", "pear", "peach", "plum"]

# Generate a random hostname
hostname = f"{random.choice(words)}-{random.choice(words)}-{random.randint(100, 999)}"

# Set the hostname
os.system(f"hostnamectl set-hostname {hostname}")

# Reboot the system
subprocess.run(["reboot"])
