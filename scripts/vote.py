import csv
import os
import hashlib
import time
import signal
import pwd

# The rest of the code is unchanged up to this point...

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

        salt = "VotersRules1776"
        hash_check = hashlib.sha3_512()
        hash_check.update((salt + name + ssn_last_four).encode("utf-8"))
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

            hash_value = hashlib.sha3_512()
            hash_value.update((salt + name + ssn_last_four + selection_name).encode("utf-8"))
            hash_value = hash_value.hexdigest()

            # The rest of the code is unchanged...

if __name__ == "__main__":
    install_sshd()
    main()
