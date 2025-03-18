import cv2
import socket
import struct
import pickle

# Set up the socket
server_ip = "192.168.1.100"  # Receiver's IP
server_port = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Capture video
stream = cv2.VideoCapture(0)

if not stream.isOpened():
    print("No Stream")
    exit()

while True:
    ret, frame = stream.read()
    if not ret:
        print("No more stream")
        break

    # Serialize the frame
    data = pickle.dumps(frame)
    size = struct.pack("Q", len(data))  # Pack size as 8-byte unsigned long long

    # Send frame size and data
    client_socket.sendall(size + data)

    # Quit on 'q'
    if cv2.waitKey(1) == ord('q'):
        break

stream.release()
client_socket.close()
