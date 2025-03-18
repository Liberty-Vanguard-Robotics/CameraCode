import cv2
import socket
import struct
import pickle

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 9999))  # Listen on all interfaces
server_socket.listen(1)
print("Waiting for connection...")

conn, addr = server_socket.accept()
print(f"Connected to {addr}")

while True:
    # Receive frame size
    data_size = struct.calcsize("Q")
    packed_size = conn.recv(data_size)
    if not packed_size:
        break

    size = struct.unpack("Q", packed_size)[0]

    # Receive frame data
    data = b""
    while len(data) < size:
        data += conn.recv(size - len(data))

    frame = pickle.loads(data)
    cv2.imshow("Received Stream", frame)

    # Quit on 'q'
    if cv2.waitKey(1) == ord('q'):
        break

conn.close()
server_socket.close()
cv2.destroyAllWindows()
