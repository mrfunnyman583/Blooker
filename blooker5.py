import subprocess
import sys
import re

REQUIRED_PACKAGES = ['python3-pip', 'python3-dev', 'libffi-dev', 'libssl-dev']

def check_packages():
    return [pkg for pkg in REQUIRED_PACKAGES if not is_package_installed(pkg)]

def is_package_installed(package):
    try:
        subprocess.check_output(['dpkg', '-s', package], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def display_reminder():
    missing = check_packages()
    if missing:
        print("Please install the following packages to use Blooker:")
        print('\n'.join(missing))
        sys.exit(1)
    else:
        print("All required packages are installed. You can use Blooker.")

def get_network_interfaces():
    try:
        output = subprocess.check_output(['ip', '-o', 'link', 'show']).decode()
        interfaces = [line.split(':')[1].strip() for line in output.strip().split('\n')]
        return interfaces
    except subprocess.CalledProcessError:
        print("Error retrieving network interfaces.")
        sys.exit(1)

def get_network_info(interface):
    try:
        output = subprocess.check_output(['ip', 'addr', 'show', interface]).decode()
        ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', output)
        mac_match = re.search(r'link/ether ([0-9a-f:]+)', output)

        ip_address = ip_match.group(1) if ip_match else "N/A"
        subnet = ip_match.group(2) if ip_match else "N/A"
        mac_address = mac_match.group(1) if mac_match else "N/A"

        return ip_address, mac_address, subnet
    except subprocess.CalledProcessError:
        print(f"Error retrieving information for interface {interface}.")
        return None, None, None

def get_network_creator(mac_address):
    for interface in get_network_interfaces():
        _, mac, _ = get_network_info(interface)
        if mac and mac.lower() == mac_address.lower():
            return interface
    return None

def display_blooker_help():
    print("""Blooker - Network Information Tool
Usage:
  blooker start                      Start scanning and match a MAC address
  blooker interfaces                 List available network interfaces
  blooker info [interface]          Get detailed info on a network interface
  blooker scan                      Perform a network scan
  blooker ping [ip_address]         Ping a specific IP address
  blooker traceroute [destination]  Run traceroute to a destination
  blooker bluetooth                 List Bluetooth devices
  blooker bluetooth-scan            Scan for nearby Bluetooth devices
  blooker help                      Display this help message
""")

def start_scanning():
    mac_address = input("Enter the MAC address of the network creator: ").strip()
    interface = get_network_creator(mac_address)
    if interface:
        print(f"The network creator with MAC address {mac_address} is on interface {interface}.")
    else:
        print(f"No interface found with MAC address {mac_address}.")

def list_interfaces():
    interfaces = get_network_interfaces()
    print("Available network interfaces:")
    for iface in interfaces:
        print(f"- {iface}")

def get_interface_info(interface):
    ip, mac, subnet = get_network_info(interface)
    print(f"""Interface Information:
Interface:   {interface}
IP Address:  {ip}
MAC Address: {mac}
Subnet:      {subnet}
""")

def scan_network():
    try:
        ip, _, subnet = get_network_info('eth0')  # Or make this dynamic
        if ip == "N/A":
            print("Could not detect IP. Please use a valid interface.")
            return
        cidr = f"{ip}/{subnet}"
        output = subprocess.check_output(["nmap", "-sn", cidr]).decode()
        print(output)
    except subprocess.CalledProcessError:
        print("Error scanning the network.")
        sys.exit(1)

def ping_ip(ip_address):
    try:
        output = subprocess.check_output(["ping", "-c", "4", ip_address]).decode()
        print(output)
    except subprocess.CalledProcessError:
        print(f"Error pinging IP {ip_address}.")
        sys.exit(1)

def traceroute(destination):
    try:
        output = subprocess.check_output(["traceroute", destination]).decode()
        print(output)
    except subprocess.CalledProcessError:
        print(f"Error tracing route to {destination}.")
        sys.exit(1)

def view_bluetooth_devices():
    try:
        output = subprocess.check_output(["hcitool", "dev"]).decode()
        print(output)
    except subprocess.CalledProcessError:
        print("Error viewing Bluetooth devices.")
        sys.exit(1)

def scan_bluetooth_devices():
    try:
        output = subprocess.check_output(["hcitool", "scan"]).decode()
        print(output)
    except subprocess.CalledProcessError:
        print("Error scanning Bluetooth devices.")
        sys.exit(1)

def main():
    args = sys.argv
    if len(args) < 2:
        display_blooker_help()
        return

    command = args[1]
    if command == "start":
        start_scanning()
    elif command == "interfaces":
        list_interfaces()
    elif command == "info" and len(args) == 3:
        get_interface_info(args[2])
    elif command == "scan":
        scan_network()
    elif command == "ping" and len(args) == 3:
        ping_ip(args[2])
    elif command == "traceroute" and len(args) == 3:
        traceroute(args[2])
    elif command == "bluetooth":
        view_bluetooth_devices()
    elif command == "bluetooth-scan":
        scan_bluetooth_devices()
    else:
        display_blooker_help()

if __name__ == "__main__":
    display_reminder()
    try:
        main()
    except KeyboardInterrupt:
        print("\nBlooker terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
