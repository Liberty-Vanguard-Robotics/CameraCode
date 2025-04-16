# import cv2
# import socket
# import struct
# import pickle

# # Set up the socket
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(("0.0.0.0", 9999))  # Listen on all interfaces
# server_socket.listen(1)
# output_width, output_height = 640, 480
# print("Waiting for connection...")

# conn, addr = server_socket.accept()
# print(f"Connected to {addr}")

# while True:
#     try:
#     # Receive frame size
#         packed_size = conn.recv(8)
#         if not packed_size:
#             continue
#         size = struct.unpack("Q", packed_size)[0]   
#         # Receive frame data
#         data = b""
#         while len(data) < size:
#             data += conn.recv(size - len(data))
    
#         # Deserialize the data (it was serialized using pickle)
#         frame = pickle.loads(data)

#         # If frame was JPEG compressed, we need to decode it
#         frame = cv2.imdecode(frame, cv2.IMREAD_GRAYSCALE)  # Assuming grayscale frames
#     except Exception as e:
#         print(f"Frame decode error: {e}")
#         continue 
#     if frame is None:
#         print("Failed to decode frame.")
#         break

#     # Resize frame to the desired output size
#     frame_resized = cv2.resize(frame, (output_width, output_height))

#     # Display the frame
#     cv2.imshow("Received Stream", frame_resized)

#     # Quit on 'q'
#     if cv2.waitKey(1) == ord('q'):
#         break

# # Close connections
# conn.close()
# server_socket.close()
# cv2.destroyAllWindows()

import cv2
import socket
import struct
import pickle

# ======= CONFIG =======
HOST = "0.0.0.0"
PORT = 9999
MAX_FRAME_SIZE = 1_000_000  # 1MB limit
OUTPUT_WIDTH, OUTPUT_HEIGHT = 640, 480

# ======= UTILITY =======
def recvall(sock, count):
    """Receive exactly 'count' bytes from socket."""
    data = b''
    while len(data) < count:
        try:
            packet = sock.recv(count - len(data))
        except Exception as e:
            print(f"Socket recv error: {e}")
            return None
        if not packet:
            return None
        data += packet
    return data

# ======= MAIN SERVER =======
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Listening on {HOST}:{PORT}...")
conn, addr = server_socket.accept()
print(f"Connected to {addr}")

while True:
    try:
        packed_size = recvall(conn, 8)
        if not packed_size:
            print("Connection closed or no size received.")
            break

        size = struct.unpack("Q", packed_size)[0]
        if size <= 0 or size > MAX_FRAME_SIZE:
            print(f"Invalid frame size: {size}")
            continue

        data = recvall(conn, size)
        if not data:
            print("No data received.")
            break

        # Deserialize and decode
        try:
            frame_data = pickle.loads(data)
            frame = cv2.imdecode(frame_data, cv2.IMREAD_GRAYSCALE)
        except Exception as e:
            print(f"Frame decode error: {e}")
            continue

        if frame is None:
            print("Decoded frame is empty.")
            continue

        frame_resized = cv2.resize(frame, (OUTPUT_WIDTH, OUTPUT_HEIGHT))
        cv2.imshow("Received Stream", frame_resized)

    except Exception as e:
        print(f"Unexpected error: {e}")
        continue

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ======= CLEANUP =======
print("Closing connection.")
conn.close()
server_socket.close()
cv2.destroyAllWindows()
