import socket
import time
import uuid


def send_request(dest_ip):
    # Send the request to the proxy server
    proxy_host = socket.gethostname()
    proxy_port = 12345
    request = f"GET / HTTP/1.1\r\nHost: {dest_ip}\r\n\r\n"
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((proxy_host, proxy_port))
    except Exception as e:
        print(f"Error connecting to proxy server: {str(e)}")
        return

    # Send request to proxy server
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{current_time} - Sending request to proxy server")
    start_time = time.time()
    client_socket.sendall(request.encode())

    # Receive response from proxy server
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data
    end_time = time.time()

    # Display response and round-trip time
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{current_time} - Received response from proxy server")
    print(f"Response: {response.decode()}")
    print(f"Round-trip time: {(end_time - start_time) * 1000} ms")

    # Display physical MAC address
    mac_address = ':'.join(format(uuid.getnode(), '012x')[
                           i:i+2] for i in range(0, 12, 2))
    print(f"Physical MAC address: {mac_address}")

    # Close socket
    client_socket.close()


def main():
    # Get website IP from user input
    dest_ip = input("Enter website IP address: ")

    # Send request to proxy server and handle response
    send_request(dest_ip)


if __name__ == '__main__':
    main()
