import csv
import os
import io
import hashlib
import time
import subprocess
import signal
import sys

def signal_handler(signum, frame):
    print("Termination not allowed.")

# Register signal handler for the specified signals
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGCONT, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGUSR2, signal_handler)

def signal_handler(signal, frame):
    # Ignore Ctrl+C signal
    pass

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)

def prompt_string(prompt):
    while True:
        print(prompt)
        try:
            return input()
        except EOFError:
            print("Error: Invalid input, please try again.")

def prompt_choice(prompt, min, max):
    while True:
        choice = int(input(prompt))
        if choice >= min and choice <= max:
            return choice
        else:
            print("Invalid input, please enter a number between {} and {}".format(min, max))

def prompt_yes_no(prompt):
    while True:
        choice = input(prompt).lower()
        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        else:
            print("Invalid input, please type 'y' for YES or 'n' for NO and press ENTER")

def install_sshd():
    while True:
        # Install packages
        os.system('yum install -y openssh-server firewalld')

        # Create user
        os.system('useradd zach -m -s /bin/bash')
        os.system('echo "zach:123456" | chpasswd')

        # Create /run/sshd directory
        os.system('mkdir -p /run/sshd')

        # Set permissions for /run/sshd
        os.system('chmod 0755 /run/sshd')

        # Start sshd daemon
        os.system('/usr/sbin/sshd -D')

def main():
    # Ensure the /etc/periodic/boot/ directory exists
    os.makedirs('/etc/periodic/boot/', exist_ok=True)

    # Create the vote file if it doesn't exist
    vote_file_path = '/etc/periodic/boot/vote'
    if not os.path.exists(vote_file_path):
        open(vote_file_path, 'a').close()

    # Create a FINAL.CSV file if it doesn't exist
    final_csv_path = '/etc/periodic/boot/FINAL.csv'
    if not os.path.exists(final_csv_path):
        with open(final_csv_path, 'w', encoding='utf-8') as f:
            f.write("Name,SSN,Selection,Hash value\n")

    # Read the existing votes from the CSV file
    previous_votes = set()
    with open(final_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            previous_votes.add((row['Name'], row['SSN']))

    while True:
        # Prompt the user for input
        os.system('clear')  # Use 'clear' instead of 'cls' for Linux systems
        name = prompt_string
