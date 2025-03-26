import socket

received_data = {}  # Dictionary to store received information

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))
server_socket.listen(5)  # Allow multiple pending connections

print("Server is listening for connections...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    
    data = client_socket.recv(1024).decode('utf-8')
    if data:
        print(f"Received Data: {data}")
        
        # Store data in dictionary, grouping by client address
        if addr in received_data:
            received_data[addr].append(data)  # Append data if client has sent before
        else:
            received_data[addr] = [data]  # Create a new list for new clients

    client_socket.close()