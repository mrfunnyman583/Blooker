Blooker
Blooker is a versatile network information tool built for network scanning, interface listing, IP pinging, tracerouting, and Bluetooth device scanning. It provides a command-line interface and leverages Python subprocess calls, Nmap, and Bluetooth utilities. Blooker helps gather network details, troubleshoot issues, and explore connected devices.

Features
Network scanning to discover hosts and open ports
Interface listing to view available network interfaces
IP pinging to check the reachability of a specific IP address
Tracerouting to trace the path taken by packets to a destination
Bluetooth device scanning to discover nearby devices
Installation
To install and use Blooker, follow these steps:

Clone the Blooker repository: git clone https://github.com/mrfunnyman583/blooker.git
Navigate to the project directory: cd blooker
Install the required packages: pip install -r requirements.txt
Usage
To run Blooker, use the following command: python blooker.py [command] [options]

Available commands:

start: Start the scanning process and prompt for a network creator's MAC address
interfaces: List available network interfaces
info [interface]: Get detailed information about a specific network interface
scan: Perform a network scan
ping [ip_address]: Ping a specific IP address
traceroute [destination]: Perform a traceroute to a specific destination
bluetooth: View Bluetooth devices
bluetooth-scan: Scan for nearby Bluetooth devices
For more details on each command and their options, run python blooker.py --help.

Contributions
Contributions to Blooker are welcome! Feel free to submit bug reports, suggest new features, or contribute code through pull requests.

License
Blooker is licensed under the MIT License. See the LICENSE file for more details.

Disclaimer
Use Blooker responsibly and respect applicable laws and regulations. The authors and contributors of Blooker are not responsible for any misuse or damages caused by its usage.
