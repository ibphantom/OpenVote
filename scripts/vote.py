# We start by importing the required libraries for this script.
# We start by importing the required libraries for this script.
import csv
import os
import hashlib
import time
import signal
import pwd

# This function is used to handle signals.
def signal_handler(signum, frame):
    # Map the signal numbers to their names
    signal_names = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                        if v.startswith('SIG') and not v.startswith('SIG_'))

    # This message will be printed when there is an attempt to terminate the script.
    print("Received signal: {}".format(signal_names[signum]))
    if signum in [signal.SIGINT, signal.SIGTSTP]:
        print("Termination not allowed.")
        return
    print("Signal not handled.")

# Registering the signal_handler function for specified signals.
# These signals include interrupt, termination, hangup, continue, and user-defined signals.
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGCONT, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGUSR2, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)

# This function prompts the user for a string input and handles errors for invalid or empty input.
def prompt_string(prompt):
    while True:
        # Print the input prompt.
        print(prompt)
        try:
            # Try to get user input and strip whitespace.
            value = input().strip()
            if not value:
                # Raise a ValueError if the input is empty.
                raise ValueError("Input cannot be empty.")
            return value
        except ValueError as e:
            # If a ValueError was raised, print the error message.
            print("Error:", str(e))

# This function prompts the user to choose an option, ensuring it is within the valid range.
def prompt_choice(prompt, min_value, max_value):
    while True:
        try:
            # Try to get user input and convert it to an integer.
            choice = int(input(prompt))
            if min_value <= choice <= max_value:
                # If the choice is within the valid range, return the choice.
                return choice
            else:
                # If the choice is not within the valid range, print an error message.
                print("Invalid input, please enter a number between {} and {}".format(min_value, max_value))
        except ValueError:
            # If the user input could not be converted to an integer, print an error message.
            print("Invalid input, please enter a valid integer.")

# This function prompts the user for a Yes/No response, accepting only valid inputs.
def prompt_yes_no(prompt):
    while True:
        # Convert the user's input to lowercase.
        choice = input(prompt).lower()
        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        else:
            print("Invalid input, please type 'y' for YES or 'n' for NO and press ENTER")

# This function installs and starts the SSH service, and creates a new user if necessary.
def install_sshd():
    # Create the '/VOTE/' directory if it doesn't exist.
    os.makedirs('/VOTE/', exist_ok=True)
    if os.path.exists('/VOTE/sshd_installed'):
        print("SSH and user setup already completed.")
        return

    # Check if the user 'zach' exists.
    try:
        pwd.getpwnam('zach')
        print("User zach already exists.")
    except KeyError:
        print("User zach not found. Creating user zach...")
        os.system('useradd zach -m -s /bin/bash')  # Create the user 'zach'.
        os.system('echo "zach:123456" | chpasswd')  # Set '123456' as the password for 'zach'.

    # Prohibit root login via SSH.
    print("Configuring SSH to disallow root login...")
    os.system('sed -i "s/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/g" /etc/ssh/sshd_config')

    # Check the status of the SSH service.
    ssh_service_status = os.system('service ssh status > /dev/null 2>&1')
    if ssh_service_status == 0:
        print("SSH service is already running.")
    else:
        print("Starting SSH service...")
        os.system('service ssh start')  # Start the SSH service.

    # Write 'done' to the file '/VOTE/sshd_installed' to indicate that the SSH service has been installed.
    with open('/VOTE/sshd_installed', 'w') as f:
        f.write('done')

# This is the main function that handles the voting process.
def main():
    # Create the '/VOTE/' directory if it doesn't exist.
    os.makedirs('/VOTE/', exist_ok=True)

    # Remove '/VOTE/client_info.txt' and '/VOTE/sshd_installed' files if they exist.
    os.remove('/VOTE/client_info.txt')
    os.remove('/VOTE/sshd_installed')

    # This code block initializes the voting CSV files if they don't exist.
    vote_file_path = '/VOTE/vote.csv'
    if not os.path.exists(vote_file_path):
        with open(vote_file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Vote', 'Hash'])

    final_csv_path = '/VOTE/FINAL.csv'
    count_csv_path = '/VOTE/count.csv'

    if not os.path.exists(final_csv_path):
        with open(final_csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Hash'])

    # Create a set to store the hash of each vote.
    previous_votes = set()

    # Add the hash of each vote from the final CSV file to the set.
    with open(final_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            previous_votes.add(row['Hash'])

    # This while loop allows users to vote.
    while True:
        # Clear the console.
        os.system('clear')

        # Get the user's name and the last 4 digits of their SSN.
        name = prompt_string("What is your name? ")
        ssn_last_four = prompt_string("What are the last 4 digits of your SSN? ")

        # Generate a hash from the user's information.
        salt = "VotersRules1776"
        hash_check = hashlib.sha3_512()
        hash_check.update((salt + name + ssn_last_four).encode("utf-8"))
        hash_check = hash_check.hexdigest()

        # Check if the user has already voted.
        if hash_check in previous_votes:
            print("You have already voted.")
            time.sleep(2)
            continue

        # This while loop allows users to select an option and confirms their selection.
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

            print("You selected:\n")

            print("Name: {}\n".format(name).center(50))
            print("SSN: {}\n".format(ssn_last_four).center(50))
            print("Selection: {}\n\n".format(selection_name).center(50))
            print("Hash value: {}".format(hash_check).center(50))

            is_correct = prompt_yes_no("Are these selections correct? (Press Y for Yes and N for No) ")

            if is_correct:
                os.system('clear')
                print("Your Confirmation Receipt is now Printing".center(50))
                time.sleep(3)

                with open(final_csv_path, "a", encoding="utf-8", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([hash_check])

                with open(vote_file_path, "a", encoding="utf-8", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([selection_name, hash_check])

                if not os.path.exists(count_csv_path):
                    with open(count_csv_path, 'w', encoding='utf-8', newline='') as f:
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
                print("Please try again.")

if __name__ == "__main__":
    install_sshd()
    main()
