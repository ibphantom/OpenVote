import csv
import os
import hashlib
import time
import signal
import pwd

# A function to handle signals, preventing termination.
def signal_handler(signum, frame):
    print("Termination not allowed.")

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

# Function to prompt the user for a string input, with error handling for invalid input
def prompt_string(prompt):
    while True:
        print(prompt)
        try:
            return input()
        except EOFError:
            print("Error: Invalid input, please try again.")

# Function to prompt the user to choose an option, ensuring it is within the valid range
def prompt_choice(prompt, min, max):
    while True:
        choice = int(input(prompt))
        if choice >= min and choice <= max:
            return choice
        else:
            print("Invalid input, please enter a number between {} and {}".format(min, max))

# Function to prompt the user for a Yes/No response, accepting only valid inputs
def prompt_yes_no(prompt):
    while True:
        choice = input(prompt).lower()
        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        else:
            print("Invalid input, please type 'y' for YES or 'n' for NO and press ENTER")

# Function to install and start SSH service, and create a new user if necessary
def install_sshd():
    os.makedirs('/VOTE/', exist_ok=True)
    if os.path.exists('/VOTE/sshd_installed'):
        print("SSH and user setup already completed.")
        return

    try:
        pwd.getpwnam('zach')
        print("User zach already exists.")
    except KeyError:
        print("User zach not found. Creating user zach...")
        # prompt for a password
        password = prompt_string("Enter a password for the user 'zach':")
        os.system('useradd zach -m -s /bin/bash')
        os.system(f'echo "zach:{password}" | chpasswd')

    ssh_service_status = os.system('service ssh status > /dev/null 2>&1')
    if ssh_service_status == 0:
        print("SSH service is already running.")
    else:
        print("Starting SSH service...")
        os.system('service start ssh')

    with open('/VOTE/sshd_installed', 'w') as f:
        f.write('done')

# Main function that handles the voting process
def main():
    os.makedirs('/VOTE/', exist_ok=True)
    vote_file_path = '/VOTE/vote'
    if not os.path.exists(vote_file_path):
        open(vote_file_path, 'a').close()

    final_csv_path = '/VOTE/FINAL.csv'
    if not os.path.exists(final_csv_path):
        with open(final_csv_path, 'w', encoding='utf-8') as f:
            f.write("Hash value\n")  # Only store the hash value

    previous_votes = set()
    with open(final_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            previous_votes.add(row['Hash value'])

    while True:
        os.system('clear')
        name = prompt_string("What is your name? ")
        ssn_last_four = prompt_string("What are the last 4 digits of your SSN? ")

        hash_check = hashlib.sha256()
        hash_check.update(name.encode("utf-8"))
        hash_check.update(ssn_last_four.encode("utf-8"))
        hash_check = hash_check.hexdigest()

        if hash_check in previous_votes:
            print("You have already voted.")
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

            selection_name = {
                1: "Option 1",
                2: "Option 2",
                3: "Option 3",
            }[selection]

            os.system('clear')

            hash_value = hashlib.sha256()
            hash_value.update(name.encode("utf-8"))
            hash_value.update(ssn_last_four.encode("utf-8"))
            hash_value.update(selection_name.encode("utf-8"))
            hash_value = hash_value.hexdigest()

            print("You selected:\n")

            print("Name: {}\n".format(name).center(50))
            print("SSN: {}\n".format(ssn_last_four).center(50))
            print("Selection: {}\n\n".format(selection_name).center(50))
            print("Hash value: {}".format(hash_value).center(50))

            is_correct = prompt_yes_no("Are these selections correct? (Press Y for Yes and N for No) ")

            if is_correct:
                os.system('clear')
                print("Your Confirmation Receipt is now Printing")
                time.sleep(3)

                with open(final_csv_path, "a", encoding="utf-8") as f:
                    f.write("{}\n".format(hash_value))

                break  
            else:
                print("Please try again.")

if __name__ == "__main__":
    install_sshd()
    main()
