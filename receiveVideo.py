import socket
import cv2
import pickle
import struct

def receive_video():
    # Setup server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.168.2', 65432))
    server_socket.listen(1)
    print("Server listening on port 65432...")

    conn, addr = server_socket.accept()
    print(f'Connection from {addr} established.')

    data = b""
    payload_size = struct.calcsize("L")

    while True:
        # Retrieve message size first
        while len(data) < payload_size:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += conn.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize and decode the frame
        frame = pickle.loads(frame_data)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # Display the frame
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close connections
    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()

# Run the server
receive_video()
