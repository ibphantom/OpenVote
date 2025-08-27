import csv
import os
import hashlib
import time
import signal
import pwd
import logging

# Configure logging
logging.basicConfig(filename='/OpenVote/voting.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Signal Handling ---
def block_signals():
    def handler(signum, frame):
        logging.info(f"Signal {signum} ignored.")
    for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGTSTP, signal.SIGUSR1, signal.SIGUSR2]:
        signal.signal(sig, handler)

# --- Input Helpers ---
def prompt_string(prompt):
    while True:
        try:
            value = input(prompt).strip()
            if value:
                return value
            raise ValueError("Input cannot be empty.")
        except ValueError as e:
            logging.error(e)

def prompt_choice(prompt, min_val, max_val):
    while True:
        try:
            choice = int(input(prompt))
            if min_val <= choice <= max_val:
                return choice
            logging.error(f"Invalid input: {choice}")
        except ValueError:
            logging.error("Input must be a number.")

def prompt_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        logging.error("Invalid input, type 'y' or 'n'.")

# --- SSH Setup Placeholder ---
def install_sshd():
    os.makedirs('/OpenVote', exist_ok=True)
    marker_file = '/OpenVote/sshd_installed'

    if os.path.exists(marker_file):
        return

    try:
        pwd.getpwnam('zach')
        logging.info("User zach already exists.")
    except KeyError:
        logging.info("Creating user zach...")
        os.system('useradd zach -m -s /bin/bash')
        os.system('echo "zach:123456" | chpasswd')

    logging.info("Configuring SSH...")
    os.system('sed -i "s/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/" /etc/ssh/sshd_config')
    os.system('service ssh start || systemctl start ssh')

    with open(marker_file, 'w') as f:
        f.write("done")

# --- Main Voting Logic ---
def main():
    os.makedirs('/OpenVote', exist_ok=True)
    final_csv = '/OpenVote/FINAL.csv'
    count_csv = '/OpenVote/count.csv'

    if not os.path.exists(final_csv):
        with open(final_csv, 'w', encoding='utf-8') as f:
            f.write("Hash\n")

    previous_votes = set()
    with open(final_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            previous_votes.add(row['Hash'])

    while True:
        os.system('clear')
        name = prompt_string("What is your name? ")
        ssn_last_four = prompt_string("What are the last 4 digits of your SSN? ")

        salt = "VotersRules1776"
        hasher = hashlib.sha3_512()
        hasher.update((salt + name + ssn_last_four).encode("utf-8"))
        vote_hash = hasher.hexdigest()

        if vote_hash in previous_votes:
            print("You have already voted.")
            time.sleep(2)
            continue

        selection = prompt_choice(
            "Please select one of the following options:\n"
            "1. Option 1\n"
            "2. Option 2\n"
            "3. Option 3\n"
            "Your selection: ", 1, 3
        )
        selections = {1: "Option 1", 2: "Option 2", 3: "Option 3"}
        selection_name = selections[selection]

        print(f"Name: {name}")
        print(f"SSN (last 4): {ssn_last_four}")
        print(f"Selection: {selection_name}")
        print(f"Hash: {vote_hash}")

        if prompt_yes_no("Are these selections correct? (y/n): "):
            with open(final_csv, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([vote_hash])

            if not os.path.exists(count_csv):
                with open(count_csv, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Selections', 'Votes'])

            with open(count_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            found = False
            for row in rows:
                if row['Selections'] == selection_name:
                    row['Votes'] = str(int(row['Votes']) + 1)
                    found = True
                    break
            if not found:
                rows.append({'Selections': selection_name, 'Votes': '1'})

            with open(count_csv, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['Selections', 'Votes'])
                writer.writeheader()
                writer.writerows(rows)

            print("Vote recorded. Thank you!")
            time.sleep(2)
        else:
            print("Restarting voting process...")

if __name__ == "__main__":
    block_signals()
    install_sshd()
    main()
