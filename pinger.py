import subprocess
import tkinter as tk
from tkinter import Label, Button, Frame
import threading
import re
import requests

# Function to get public IP address
def get_public_ip():
    try:
        # Fetch public IP using a public API
        response = requests.get('https://api.ipify.org')
        public_ip = response.text
        return public_ip
    except Exception as e:
        print("Error fetching public IP:", e)
        return "N/A"

# Function to perform traceroute
def tracert_ip(ip):
    try:
        # Run the traceroute command
        result = subprocess.run(['tracert', ip], capture_output=True, text=True, timeout=90)
        # Print the traceroute result
        print(result.stdout)
    except Exception as e:
        print("Error:", e)

# Add IP addresses and hostnames to be pinged along with their labels
data = [
    {'ip': '8.8.8.8', 'hostname': 'Google'},
    ]

def ping_ip(ip, label, rt_label):
    try:
        while True:
            # Run the ping command
            result = subprocess.run(['ping', '-n', '1', ip], capture_output=True, text=True, timeout=5)
            match = re.search(r"time=(\d+)ms", result.stdout)
            if match:
                round_trip_time = int(match.group(1))  # Extract round-trip time as an integer
                round_trip_time_str = f"{round_trip_time}ms"
                if round_trip_time > 200:
                    rt_label.config(fg='red')  # Set font color to red if round-trip time exceeds 200 milliseconds
                elif round_trip_time > 100:
                    rt_label.config(fg='yellow')  # Set font color to yellow if round-trip time exceeds 100 milliseconds
                else:
                    rt_label.config(fg='white')   # Set font color to white if round-trip time is 100 milliseconds or less
            else:
                round_trip_time_str = 'Round-trip time not found in the output.'
                rt_label.config(fg='white')   # Set font color to white if round-trip time is not found
            # Extract time information
            if result.returncode == 0:
                label.config(text="Status: Online", bg='#008000')  # Set label text and background to green for online
            else:
                label.config(text="Status: Offline", bg='#800000')    # Set label text and background to red for offline

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

# Create a label to display public IP address
public_ip_label = Label(root, text=f"Public IP: {get_public_ip()}", bg='#303030', fg='white', font=('Arial', 12, 'bold'))
public_ip_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Create a list to store labels and round-trip time labels
labels = []

# Create a frame for each IP and arrange them into rows
for i, entry in enumerate(data, start=1):
    hostname = entry['hostname']
    ip = entry['ip']
    
    frame = Frame(root, bg='#303030')
    frame.grid(row=i, column=0, padx=5, pady=5, sticky='ew')  # Grid layout with sticky option to expand horizontally

    host_label = Label(frame, text=f"{hostname} ({ip})", bg='#808080', fg='white', width=25)  # Set label background to dark gray
    host_label.pack(side=tk.LEFT, padx=(5, 10), pady=5)  # Adjust padding for host label

    status_label = Label(frame, text="Status: Online", bg='#008000', fg='white', width=15)
    status_label.pack(side=tk.LEFT, padx=(0, 10), pady=5)  # Adjust padding for status label

    rt_label = Label(frame, text="Time: 0ms", bg='#303030', fg='white', width=35)  # Set label background to dark gray
    rt_label.pack(side=tk.LEFT, padx=(0, 10), pady=5)  # Adjust padding for round-trip time label

    threading.Thread(target=ping_ip, args=(ip, status_label, rt_label)).start()

    tracert_button = Button(frame, text="Tracert", bg='#606060', fg='white', command=lambda ip=ip: tracert_ip(ip))  # Set button background to gray
    tracert_button.pack(side=tk.LEFT, padx=(0, 5), pady=5)  # Adjust padding for trace button

# Run the Tkinter event loop
root.mainloop()
