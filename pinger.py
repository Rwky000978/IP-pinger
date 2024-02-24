import subprocess
import tkinter as tk
from tkinter import Label, Button
import threading
import re

# Add IP addresses and hostnames to be pinged along with their labels
data = [
   {'ip': '8.8.8.8', 'hostname': 'Google'}
]

def ping_ip(ip, label, rt_label, root):
    try:
        while True:
            # Run the ping command
            result = subprocess.run(['ping', '-n', '1', ip], capture_output=True, text=True, timeout=5)
            match = re.search(r"time=(\d+)ms", result.stdout)
            if match:
                round_trip_time = int(match.group(1))  # Extract round-trip time as an integer
                round_trip_time_str = f"{round_trip_time}ms"
                if round_trip_time > 100:
                    rt_label.config(fg='yellow')  # Set font color to yellow if round-trip time exceeds 100 milliseconds
                else:
                    rt_label.config(fg='white')   # Set font color to white if round-trip time is below or equal to 100 milliseconds
            else:
                round_trip_time_str = 'Round-trip time not found in the output.'
                rt_label.config(fg='white')   # Set font color to white if round-trip time is not found
            # Extract time information
            if result.returncode == 0:
                label.config(bg='#008000')  # Set label background to dark green for online
            else:
                label.config(bg='#800000')    # Set label background to dark red for offline

            # Update round-trip time label
            rt_label.config(text=f"Time: {round_trip_time_str}")

            # Sleep for 1 second before next ping
            threading.Event().wait(1)

    except subprocess.TimeoutExpired:
        round_trip_time_str = 'Timeout'
        label.config(bg='#808000')     # Set label background to dark yellow for timeout
        rt_label.config(fg='white')   # Set font color to white for timeout
        rt_label.config(text=f"Time: {round_trip_time_str}")

# Create the main window
root = tk.Tk()
root.title("Server Status Report - Powered by TechClone")
root.configure(bg='#303030')  # Set background color to dark gray

# Create a list to store labels and round-trip time labels
labels = []

# Create a label for each IP and arrange them into rows
for i, entry in enumerate(data, start=1):
    hostname = entry['hostname']
    ip = entry['ip']
    label = Label(root, text=f"{hostname} ({ip})", width=25, height=3, bg='#808080', fg='white')  # Set label background to dark gray
    label.grid(row=i, column=0, padx=5, pady=5)  # Grid layout
    rt_label = Label(root, text="Time: ", width=40, height=3, bg='#303030', fg='white')  # Set label background to dark gray
    rt_label.grid(row=i, column=1, padx=5, pady=5)  # Grid layout
    labels.append(label)
    threading.Thread(target=ping_ip, args=(ip, label, rt_label, root)).start()
    tracert_button = Button(root, text="Tracert", bg='#606060', fg='white', command=lambda ip=ip: tracert_ip(ip))  # Set button background to gray
    tracert_button.grid(row=i, column=2, padx=5, pady=5)  # Grid layout

# Run the Tkinter event loop
root.mainloop()
