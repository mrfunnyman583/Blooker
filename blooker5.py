import subprocess
import sys

REQUIRED_PACKAGES = ['python3-pip', 'python3-dev', 'libffi-dev', 'libssl-dev']

def check_packages():
    missing_packages = [package for package in REQUIRED_PACKAGES if not is_package_installed(package)]
    return missing_packages

def is_package_installed(package):
    try:
        subprocess.check_output(['dpkg', '-s', package])
        return True
    except subprocess.CalledProcessError:
        return False

def display_reminder():
    missing_packages = check_packages()

    if missing_packages:
        print("Please install the following packages to use Blooker:")
        print('\n'.join(missing_packages))
        sys.exit(1)  # Exit the program with an error code
    else:
        print("All required packages are installed. You can use Blooker.")

def get_network_interfaces():
    try:
        output = subprocess.check_output(['ip', 'link', 'show']).decode()
        interfaces = [line.split(':')[1].strip() for line in output.split('\n') if line.strip().startswith(" ")]
        return interfaces
    except subprocess.CalledProcessError:
        print("Error retrieving network interfaces.")
        sys.exit(1)

def get_network_info(interface):
    try:
        output = subprocess.check_output(['ip', 'addr', 'show', interface]).decode()
        parts = output.split("inet ")[1].split("/")
        ip_address = parts[0].strip()
        subnet = parts[1].split(" brd")[0].strip()
        mac_address = output.split("link/ether ")[1].split(" ")[0].strip()
        return ip_address, mac_address, subnet
    except subprocess.CalledProcessError:
        print(f"Error retrieving information for interface {interface}.")
        sys.exit(1)

def get_network_creator(mac_address):
    for interface in get_network_interfaces():
        _, mac, _ = get_network_info(interface)
        if mac.lower() == mac_address.lower():
            return interface

    return None

def display_blooker_help():
    print("Blooker - Network Information Tool")
    print("Usage:")
    print("  blooker start              Start the scanning process and prompt for a network creator's MAC address")
    print("  blooker interfaces         List available network interfaces")
    print("  blooker info [interface]   Get detailed information about a specific network interface")
    print("  blooker scan               Perform a network scan")
    print("  blooker ping [ip_address]  Ping a specific IP address")
    print("  blooker traceroute [destination]  Perform a traceroute to a specific destination")
    print("  blooker bluetooth          View Bluetooth devices")
    print("  blooker bluetooth-scan     Scan for nearby Bluetooth devices")
    print("  blooker help               Display this help message")

def start_scanning():
    mac_address = input("Enter the MAC address of the network creator: ")
    interface = get_network_creator(mac_address)

    if interface:
        print(f"The network creator with MAC address {mac_address} is associated with interface {interface}.")
    else:
        print(f"No network creator found with MAC address {mac_address}.")

def list_interfaces():
    interfaces = get_network_interfaces()
    print("Available network interfaces:")
    for interface in interfaces:
        print(interface)

def get_interface_info(interface):
    ip_address, mac_address, subnet = get_network_info(interface)
    print("Interface Information:")
    print(f"Interface: {interface}")
    print(f"IP Address: {ip_address}")
    print(f"MAC Address: {mac_address}")
    print(f"Subnet: {subnet}")

def scan_network():
    try:
        cmd = ["nmap", "-sn", "192.168.1.0/24"]  # Update the IP range as per your network configuration
        output = subprocess.check_output(cmd).decode()
        print(output)
    except subprocess.CalledProcessError:
        print("Error scanning the network.")
        sys.exit(1)

def ping_ip(ip_address):
    try:
        cmd = ["ping", "-c", "4", ip_address]
        output = subprocess.check_output(cmd).decode()
        print(output)
    except subprocess.CalledProcessError:
        print(f"Error pinging IP address {ip_address}.")
        sys.exit(1)

def traceroute(destination):
    try:
        cmd = ["traceroute", destination]
        output = subprocess.check_output(cmd).decode()
        print(output)
    except subprocess.CalledProcessError:
        print(f"Error performing traceroute to {destination}.")
        sys.exit(1)

def view_bluetooth_devices():
    try:
        cmd = ["hcitool", "dev"]
        output = subprocess.check_output(cmd).decode()
        print(output)
    except subprocess.CalledProcessError:
        print("Error viewing Bluetooth devices.")
        sys.exit(1)

def scan_bluetooth_devices():
    try:
        cmd = ["hcitool", "scan"]
        output = subprocess.check_output(cmd).decode()
        print(output)
    except subprocess.CalledProcessError:
        print("Error scanning for Bluetooth devices.")
        sys.exit(1)

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "start":
            start_scanning()
        elif command == "interfaces":
            list_interfaces()
        elif command == "info" and len(sys.argv) == 3:
            get_interface_info(sys.argv[2])
        elif command == "scan":
            scan_network()
        elif command == "ping" and len(sys.argv) == 3:
            ping_ip(sys.argv[2])
        elif command == "traceroute" and len(sys.argv) == 3:
            traceroute(sys.argv[2])
        elif command == "bluetooth":
            view_bluetooth_devices()
        elif command == "bluetooth-scan":
            scan_bluetooth_devices()
        else:
            display_blooker_help()
    else:
        display_blooker_help()

if __name__ == "__main__":
    display_reminder()
    try:
        main()
    except KeyboardInterrupt:
        print("\nBlooker terminated by the user.")
    except Exception as e:
        print(f"An error occurred: {e}")
