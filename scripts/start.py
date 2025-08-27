#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

OPENVOTE_ROOT = Path("/OpenVote")
CLIENT_SCRIPT = OPENVOTE_ROOT / "vote.py"
SERVER_SCRIPT = OPENVOTE_ROOT / "server.py"


def main() -> int:
    try:
        role = input("Is this device a server or a client? ").strip().lower()
    except EOFError:
        print("Error: End of input reached unexpectedly.")
        return 1

    if role not in {"server", "client"}:
        print("Invalid input. Enter 'server' or 'client'.")
        return 2

    # Ensure the working tree exists
    OPENVOTE_ROOT.mkdir(parents=True, exist_ok=True)

    if role == "client":
        if not CLIENT_SCRIPT.exists():
            print(f"Missing {CLIENT_SCRIPT}.")
            return 3
        print("Launching client voting terminal.")
        return subprocess.run([sys.executable, str(CLIENT_SCRIPT)], check=False).returncode

    if role == "server":
        if not SERVER_SCRIPT.exists():
            print(f"Missing {SERVER_SCRIPT}.")
            return 4
        print("Launching server aggregator.")
        return subprocess.run([sys.executable, str(SERVER_SCRIPT)], check=False).returncode

    return 0


if __name__ == "__main__":
    sys.exit(main())
