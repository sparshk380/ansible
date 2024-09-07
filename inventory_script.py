#!/usr/bin/env python3

import json
import socket
import fcntl
import struct

# Function to fetch the actual external IP address
def get_external_ip(interface_name='eth0'):
    try:
        # Create a socket and get the IP associated with a specific network interface
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = fcntl.ioctl(
            sock.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(interface_name[:15], 'utf-8'))
        )[20:24]
        return socket.inet_ntoa(ip_address)
    except OSError:
        return "127.0.0.1"  # Return loopback if unable to get external IP

def get_local_inventory():
    # Replace 'eth0' with your network interface name if needed (use `ifconfig` or `ip a` to check)
    local_ip = get_external_ip('eth0')
    
    # Structure the inventory in JSON format expected by Ansible
    inventory = {
        "all": {
            "hosts": [local_ip],
            "vars": {
                "ansible_user": "ubuntu",  # Replace with your SSH username
                "ansible_connection": "ssh",
                "ansible_ssh_private_key_file": "/home/ubuntu/.ssh/id_rsa"  # Path to your private SSH key
            }
        }
    }
    return inventory

if __name__ == "__main__":
    print(json.dumps(get_local_inventory(), indent=2))
