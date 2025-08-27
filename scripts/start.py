import subprocess
import os

def main():
    while True:
        try:
            device_type = input("Is this device a server or a client? ").strip().lower()
            if device_type in ("server", "client"):
                break
            else:
                print("Invalid input. Please enter either 'server' or 'client'.")
        except EOFError:
            print("Error: End of input reached unexpectedly. Please try again.")

    if device_type == "client":
        # Ensure OpenVote directory exists
        os.makedirs('/OpenVote', exist_ok=True)

        # Startup script for vote.py
        vote_script = '/OpenVote/vote'
        with open(vote_script, 'w') as f:
            f.write('#!/bin/sh\n')
            f.write('/usr/bin/python3 /OpenVote/vote.py >> /OpenVote/vote.log 2>&1\n')
        os.chmod(vote_script, 0o755)

        print("This device is a client.")
        subprocess.run(["python3", "/OpenVote/vote.py"])

    elif device_type == "server":
        print("This device is a server.")
        subprocess.run(["python3", "server.py"])

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
