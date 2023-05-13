import tkinter as tk

# Create a full screen window
window = tk.Tk()
window.attributes('-fullscreen', True)

# Set the background color to dark grey
window.configure(bg='#404040')

# Create a button that says 'Vote' and center aligns it in the window
button = tk.Button(window, text='Vote', command=lambda: start_vote_bat())
button.config(width=200, height=100, font=("Arial", 20), bg='#404040', fg='black')
button.pack(anchor='center')

# Create a white box that asks for the user's name
name_entry = tk.Entry(window, width=20)
name_entry.pack(anchor='center')

# Start vote.py
def start_vote_bat():
    import subprocess
    subprocess.Popen('start.bat')
    window.destroy()

# Start the main loop
window.mainloop()
