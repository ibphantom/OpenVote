import keyboard
import signal

MY_SIGNAL = signal.SIGUSR1

def my_handler(signum, frame):
    print(f"Received signal {signum}")
    # do something here

# Register a signal handler for MY_SIGNAL
signal.signal(MY_SIGNAL, my_handler)

# Define a function to check for the key combination and send the signal
def check_for_signal():
    if keyboard.is_pressed('ctrl+k+r'):
        os.kill(os.getpid(), MY_SIGNAL)

# Call the check_for_signal function in a loop to detect key presses
while True:
    check_for_signal()
