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

# Create a cron job to start vote.py on boot
cron_job = f'@reboot python3 /vote.py >/dev/null 2>&1\n'

# Open the crontab file for editing and write the cron job
with open('/etc/crontab', 'a') as file:
    file.write(cron_job)

# Reboot the system
subprocess.run(["reboot"])
