# Blooker

Blooker is a network information tool for scanning networks, listing interfaces, pinging IPs, performing traceroutes, and scanning Bluetooth devices. It offers a command-line interface and utilizes Python subprocess calls, Nmap, and Bluetooth utilities. Blooker helps gather network details, troubleshoot network issues, and explore connected devices.

## Installation

To use Blooker, please make sure you have the following requirements installed:

- Python 3.6+
- python3-dev
- libffi-dev
- libssl-dev
- iputils-ping

You can install the required packages by running the following command:

pip install -r requirements.txt (Also i added bluetooth features, as it not metioned here but if u want to use them, Just install hcitool and bluez!! also u need a device for bluetooth devices that supports lsusb! so just a little disclamier..."
## Usage

Once you have installed the required packages, you can run Blooker using the following command:
python3 blooker5.py [command] [options] 
Available commands:

- `start`: Start the scanning process and prompt for a network creator's MAC address.
- `interfaces`: List available network interfaces.
- `info [interface]`: Get detailed information about a specific network interface.
- `scan`: Perform a network scan.
- `ping [ip_address]`: Ping a specific IP address.
- `traceroute [destination]`: Perform a traceroute to a specific destination.
- `bluetooth`: View Bluetooth devices.
- `bluetooth-scan`: Scan for nearby Bluetooth devices.
- `help`: Display the help message.

For example, to start the scanning process, you can use:

python3 blooker5.py start 
For more information and detailed usage instructions, please refer to the help message provided by the `help` command.

## Contributing

Contributions to Blooker are welcome! If you have any suggestions, bug reports, or feature requests, please feel free to open an issue or submit a pull request on the GitHub repository.

## License

Blooker is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

