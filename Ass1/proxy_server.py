import socket
import time
from urllib.parse import urlparse


def parse_request(request):
    # Split request into lines and extract URL from first line
    lines = request.encode().split('\n')
    url = lines[0].split(' ')[1]
    # Parse URL and extract IP address
    try:
        parsed_url = urlparse(url)
        dest_ip = socket.gethostbyname(parsed_url.hostname)
    except (socket.gaierror, TypeError):
        dest_ip = None
    return dest_ip


def handle_request(client_socket, client_address):
    # Receive client request
    request = client_socket.recv(1024).decode()

    # Get destination server IP address
    dest_ip = parse_request(request)
    # Connect to destination server
    dest_port = 80
    try:
        dest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest_socket.connect((dest_ip, dest_port))
    except Exception as e:
        print(f"Error connecting to destination server {dest_ip}: {str(e)}")
        client_socket.sendall(
            f"Error connecting to destination server {dest_ip}: {str(e)}".encode())
        client_socket.close()
        return

    # Send request to destination server
    dest_socket.sendall(request.encode())

    # Receive response from destination server
    response = b""
    while True:
        data = dest_socket.recv(1024)
        if not data:
            break
        response += data

    # Send response back to client
    client_socket.sendall(response)

    # Print messages to console
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{current_time} - Received request from {client_address} for {dest_ip}")
    print(f"{current_time} - Sent request to {dest_ip}")
    print(f"{current_time} - Received response from {dest_ip}")
    print(f"{current_time} - Sent response to {client_address}")

    # Close sockets
    dest_socket.close()
    client_socket.close()


def main():
    # Create socket object
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind socket to a port
    proxy_host = socket.gethostname()
    proxy_port = 12345
    proxy_socket.bind((proxy_host, proxy_port))

    # Listen for incoming connections
    proxy_socket.listen()
    print(f"Proxy server listening on {proxy_host}:{proxy_port}")
    while True:
        # Accept incoming connections
        client_socket, client_address = proxy_socket.accept()

        # Handle incoming request
        handle_request(client_socket, client_address)


if __name__ == '__main__':
    main()