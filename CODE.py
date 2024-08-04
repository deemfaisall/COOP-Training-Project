import subprocess
import ipaddress
import socket


def get_connected_subnets():
    subnets = set()

    # Get IP address of the current machine (server)
    server_ip = socket.gethostbyname(socket.gethostname())

    # Define subnet for the server's IP address (adjust subnet mask according to server ip)
    subnet_server = ipaddress.IPv4Network(f'{server_ip}/32', strict=False)

    # Add subnet to the set of subnets
    subnets.add(subnet_server)

    # Define subnet for the client's IP address (adjust as needed)
    # (not needed on server since code is going to iterate over server subnet?)
    client_ip = '172.16.253.126'  # Example client IP address
    subnet_client = ipaddress.IPv4Network(f'{client_ip}/32', strict=False)

    # Add subnet to the set of subnets
    subnets.add(subnet_client)

    return subnets


def get_computers_in_subnet(subnet):
    computers = []

    for ip in subnet.hosts():
        ip = str(ip)
        print(f'Checking {ip}...')
        # Check if host is reachable (pingable)
        result = subprocess.run(['ping', '-n', '1', '-w', '200', ip], capture_output=True, text=True)
        if result.returncode == 0:
            print(f'Pinged {ip} successfully.')
            computers.append(ip)
        else:
            print(f'Ping failed to {ip}.')

    return computers


def initiate_shutdown(computers):
    # Get IP address of the server (current machine)
    server_ip = socket.gethostbyname(socket.gethostname())

    for computer in computers:
        if computer != server_ip:
            print(f'Initiating shutdown on {computer}...')
            result = subprocess.run(['ssh', computer, 'sudo shutdown -h now'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f'Shutdown initiated successfully on {computer}.')
            else:
                print(f'Failed to initiate shutdown on {computer}: {result.stderr}')
        else:
            print(f'Skipping shutdown for server IP {computer}.')


def main():
    connected_subnets = get_connected_subnets()
    for subnet in connected_subnets:
        print(f'Computers in subnet {subnet}:')
        computers_in_subnet = get_computers_in_subnet(subnet)
        for computer in computers_in_subnet:
            print(f'  {computer}')

        # Uncomment to initiate shutdown on computers
        initiate_shutdown(computers_in_subnet)


if __name__ == '__main__':
    main()
