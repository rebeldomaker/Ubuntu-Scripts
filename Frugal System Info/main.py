# What platoform (OS) the script is running on
import platform
import subprocess

x = platform.system()
print(x)

# OS Version
os_version = subprocess.check_output("lsb_release -a", shell=True, text=True)
print(os_version)

# System uptime
uptime = subprocess.check_output("uptime -p", shell=True, text=True)
print(uptime)

# CPU details
cpu_info = subprocess.check_output("grep 'model name' /proc/cpuinfo | uniq", shell=True, text=True)
print(cpu_info)

# CPU Usage
cpu_usage = subprocess.check_output("top -bn1 | grep 'Cpu(s)'", shell=True, text=True)
print(cpu_usage)

# Memory total and usage
mem_info = subprocess.check_output("free -h", shell=True, text=True)
print(mem_info)

# Detailed RAM info (shell)
'''sudo dmidecode --type memory'''
"""GPT

It looks like you've encountered a SyntaxError when trying to run a command in Python. This specific error is because you're trying to run a shell command (sudo dmidecode --type memory) directly in the Python interpreter, which expects Python syntax, not shell commands.

To run shell commands from within Python, you need to use the subprocess module, and specifically a function like subprocess.run() or subprocess.check_output(). Also, note that running commands with sudo from within Python can be complex because sudo may prompt for a password.

Here's how you might use subprocess to run the dmidecode command without sudo (as running with sudo would typically require additional handling for password input):"""

try:
	ram_info = subprocess.check_output(["dmidecode", "--type", "memory"], text=True)
	print(ram_info)
except subprocess.CalledProcessError as e:
	print("An error occurred while trying to retrieve RAM information.")

	"""If you need to run a command with sudo, you would have to run the script itself with sudo privileges, or manage the password prompt in a different way, which can get complicated and poses security risks if not handled carefully. For security reasons, it's generally best to avoid automating sudo password input."""

# Disk usage
disk_usage = subprocess.check_output("df -h", shell=True, text=True)
print(disk_usage)

# Network
ip_address = subprocess.check_output("hostname -I", shell=True, text=True)
print(ip_address)

# Pending updates
pending_updates = subprocess.check_output("apt list --upgradable", shell=True, text=True)
print(pending_updates)

# List installed packages
'''installed_packages = subprocess.check_output("apt list --installed", shell=True, text=True)
print(installed_packages)'''

# List all the defined names belonging to the platform module

'''
x = dir(platform)
print(x)'''
