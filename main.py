import platform
import subprocess
import psutil
import GPUtil as gputil
import os
import datetime
import cpuinfo as py_cpuinfo
import netifaces
import uptime as system_uptime
import pandas as pd
import numpy as np

def main():
    # Retrieve and print the name of the operating system
    os_name = platform.system()
    print("Operating System:", os_name)

    # Execute a shell command to get the operating system version
    os_version = subprocess.check_output("lsb_release -a", shell=True, text=True)
    print("OS Version:", os_version.strip())

    # System uptime, use subprocess to execute a shell command for system uptime
    system_uptime_output = subprocess.check_output("uptime -p", shell=True, text=True)
    print("System Uptime:", system_uptime_output.strip())

    # Show today's date
    x = datetime.datetime.now()
    '''print("Date Printed on:", x)'''
    print(x.strftime("Current date: %H:%M %p %A, %d %b %Y"))

    # Get CPU information like model name using a grep command on /proc/cpuinfo
    cpu_info_output = subprocess.check_output("grep 'model name' /proc/cpuinfo | uniq", shell=True, text=True)
    print("CPU Details:", cpu_info_output.strip())

    # Print the current CPU usage as a percentage
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_usage}%")

    # Memory total and usage
    mem_info_output = subprocess.check_output("free -h", shell=True, text=True)
    print(mem_info_output)

    # Retrieve and print total, used, and available memory
    mem_info = psutil.virtual_memory()
    print(f"Total Memory: {mem_info.total >> 30} GiB")
    print(f"Used Memory: {mem_info.used >> 30} GiB")
    print(f"Available Memory: {mem_info.available >> 30} GiB")

    # Disk usage
    disk_usage_output = subprocess.check_output("df -h", shell=True, text=True)
    print(disk_usage_output)

    # List all mounted disk partitions and their usage stats, excluding loop devices
    disk_partitions = psutil.disk_partitions()
    for partition in disk_partitions:
        if not partition.device.startswith('/dev/loop'):
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Partition: {partition.device}, Mounted at: {partition.mountpoint}, Usage: {usage.percent}% full")

    # Network
    ip_address_output = subprocess.check_output("hostname -I", shell=True, text=True)
    print("IP Address:", ip_address_output.strip())

    # List GPU information
    gpus = gputil.getGPUs()
    for gpu in gpus:
        print(f"GPU: {gpu.name}, Load: {gpu.load * 100}%, Temperature: {gpu.temperature} C")

    # Current date and time
    now = datetime.datetime.now()
    print("Current Date & Time:", now)

    # CPU information using py_cpuinfo
    cpu_info = py_cpuinfo.get_cpu_info()
    print("CPU Brand:", cpu_info['brand_raw'])

    # Network interfaces and IP addresses using netifaces
    for interface in netifaces.interfaces():
        addr = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addr:
            ip_info = addr[netifaces.AF_INET][0]
            print(f"Interface: {interface}, IP Address: {ip_info['addr']}")

    # System uptime using the uptime library
    print("System Uptime (Library):", system_uptime.uptime())

    # List pending updates
    pending_updates = subprocess.check_output("apt list --upgradable", shell=True, text=True)
    print(pending_updates)

    # Try to list pending security updates, handle the case where there might be none
    try:
        security_updates = subprocess.check_output("apt list --upgradable | grep security", shell=True, text=True)
        print("Security Updates:", security_updates)
    except subprocess.CalledProcessError as e:
        print("No security updates found.")

    # Create a simple DataFrame and print it
    df = pd.DataFrame({'Numbers': range(5), 'Squares': np.square(range(5))})
    print(df)

    # Save to file
    save_output = input("Do you want to save the output to a file? (yes/no): ").lower()
    if save_output == 'yes':
        # Generate a filename with the current date and time
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"system_info_{date_str}.txt"

        # The full path for the file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, filename)

        with open(full_path, 'w') as f:
            f.write(f"Operating System: {os_name}\n")
            f.write(f"OS Version: {os_version.strip()}\n")
            f.write(f"System Uptime: {system_uptime_output.strip()}\n")
            f.write(f"CPU Details: {cpu_info_output.strip()}\n")
            f.write(f"CPU Usage: {cpu_usage}%\n")
            f.write(f"{mem_info_output}\n")
            f.write(f"Total Memory: {mem_info.total >> 30} GiB\n")
            f.write(f"Used Memory: {mem_info.used >> 30} GiB\n")
            f.write(f"Available Memory: {mem_info.available >> 30} GiB\n")
            f.write(f"{disk_usage_output}\n")
            for partition in disk_partitions:
                if not partition.device.startswith('/dev/loop'):
                    usage = psutil.disk_usage(partition.mountpoint)
                    f.write(f"Partition: {partition.device}, Mounted at: {partition.mountpoint}, Usage: {usage.percent}% full\n")
            f.write(f"IP Address: {ip_address_output.strip()}\n")
            for gpu in gpus:
                f.write(f"GPU: {gpu.name}, Load: {gpu.load * 100}%, Temperature: {gpu.temperature} C\n")
            f.write(f"Current Date & Time: {now}\n")
            f.write(f"CPU Brand: {cpu_info['brand_raw']}\n")
            for interface in netifaces.interfaces():
                addr = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addr:
                    ip_info = addr[netifaces.AF_INET][0]
                    f.write(f"Interface: {interface}, IP Address: {ip_info['addr']}\n")
            f.write(f"System Uptime (Library): {system_uptime.uptime()}\n")
            f.write(f"Pending Updates:\n{pending_updates}\n")
            # Only write security updates if the command did not fail
            if 'security_updates' in locals():
                f.write(f"Security Updates:\n{security_updates}\n")
            df_str = df.to_string(header=True, index=False)
            f.write(f"\nDataFrame:\n{df_str}\n")

        print(f"Output saved to {full_path}")

if __name__ == "__main__":
    main()
