import csv
import os
import hashlib
import time
import signal
import pwd
import logging

# Configure logging settings
logging.basicConfig(filename='voting.log', level=logging.INFO)


# A function to handle signals, preventing termination.
def signal_handler(signum, frame):
    logging.info("Termination not allowed.")


# Registering signal handler for specified signals
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGCONT, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGUSR2, signal_handler)

# Another function to ignore Ctrl+C signal
def signal_handler(signal, frame):
    pass

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)

# Function to prompt the user for a string input, with error handling for invalid or empty input
def prompt_string(prompt):
    while True:
        logging.info(prompt)
        try:
            value = input().strip()
            if not value:
                raise ValueError("Input cannot be empty.")
            return value
        except ValueError as e:
            logging.error("Error: " + str(e))

# Function to prompt the user to choose an option, ensuring it is within the valid range
def prompt_choice(prompt, min, max):
    while True:
        choice = int(input(prompt))
        if choice >= min and choice <= max:
            return choice
        else:
            logging.error("Invalid input, please enter a number between {} and {}".format(min, max))

# Function to prompt the user for a Yes/No response, accepting only valid inputs
def prompt_yes_no(prompt):
    while True:
        choice = input(prompt).lower()
        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        else:
            logging.error("Invalid input, please type 'y' for YES or 'n' for NO and press ENTER")

# Function to install and start SSH service, and create a new user if necessary
def install_sshd():
    os.makedirs('/OpenVote/', exist_ok=True)
    if os.path.exists('/OpenVote/sshd_installed'):
        logging.info("SSH and user setup already completed.")
        return

    try:
        pwd.getpwnam('zach')
        logging.info("User zach already exists.")
    except KeyError:
        logging.info("User zach not found. Creating user zach...")
        os.system('useradd zach -m -s /bin/bash')
        os.system(f'echo "zach:123456" | chpasswd')

    # Prohibit root login via SSH
    logging.info("Configuring SSH to disallow root login...")
    os.system('sed -i "s/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/g" /etc/ssh/sshd_config')

    ssh_service_status = os.system('service ssh status > /dev/null 2>&1')
    if ssh_service_status == 0:
        logging.info("SSH service is already running.")
    else:
        logging.info("Starting SSH service...")
        os.system('service ssh start')

    with open('/OpenVote/sshd_installed', 'w') as f:
        f.write('done')

# Main function that handles the voting process
def main():
    os.makedirs('/OpenVote/', exist_ok=True)
    vote_file_path = '/OpenVote/vote'
    if not os.path.exists(vote_file_path):
        open(vote_file_path, 'a').close()

    final_csv_path = '/OpenVote/FINAL.csv'
    count_csv_path = '/OpenVote/count.csv'

    if not os.path.exists(final_csv_path):
        with open(final_csv_path, 'w', encoding='utf-8') as f:
            f.write("Hash value\n")  # Only store the hash value

    previous_votes = set()

    with open(final_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            previous_votes.add(row['Hash'])

    while True:
        os.system('clear')
        name = prompt_string("What is your name? ")
        ssn_last_four = prompt_string("What are the last 4 digits of your SSN? ")

        # Move hash computation before the 'if' condition
        salt = "VotersRules1776"
        hash_check = hashlib.sha3_512()
        hash_check.update((salt + name + ssn_last_four).encode("utf-8"))
        hash_check = hash_check.hexdigest()

        if hash_check in previous_votes:
            logging.info("You have already voted.")
            time.sleep(2)
            continue

        while True:
            os.system('clear')
            selection = prompt_choice(
                "Please select one of the following options: \n"
                "1. Option 1\n"
                "2. Option 2\n"
                "3. Option 3\n"
                "Your selection: ",
                1,
                3,
            )

            selections = {
                1: "Option 1",
                2: "Option 2",
                3: "Option 3",
            }

            selection_name = selections[selection]

            os.system('clear')

            salt = "VotersRules1776"
            hash_check = hashlib.sha3_512()
            hash_check.update((salt + name + ssn_last_four).encode("utf-8"))
            hash_check = hash_check.hexdigest()

            logging.info("You selected:\n")

            logging.info("Name: {}\n".format(name).center(50))
            logging.info("SSN: {}\n".format(ssn_last_four).center(50))
            logging.info("Selection: {}\n\n".format(selection_name).center(50))
            logging.info("Hash value: {}".format(hash_check).center(50))

            is_correct = prompt_yes_no("Are these selections correct? (Press Y for Yes and N for No) ")

            if is_correct:
                os.system('clear')
                logging.info("Your Confirmation Receipt is now Printing".center(50))
                time.sleep(3)

                with open(final_csv_path, "a", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([hash_check])

                if not os.path.exists(count_csv_path):
                    with open(count_csv_path, 'w', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Selections', 'Votes'])

                with open(count_csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)

                selection_exists = False

                for row in rows:
                    if row['Selections'] == selection_name:
                        row['Votes'] = str(int(row['Votes']) + 1)
                        selection_exists = True
                        break

                if not selection_exists:
                    rows.append({'Selections': selection_name, 'Votes': '1'})

                with open(count_csv_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['Selections', 'Votes'])
                    writer.writeheader()
                    writer.writerows(rows)

                break
            else:
                logging.info("Please try again.")

if __name__ == "__main__":
    install_sshd()
    main()
