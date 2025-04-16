import cv2
import socket
import struct
import pickle

# Set up the socket
server_ip = "192.168.1.208"  # Receiver's IP
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
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Use INTER_NEAREST for fastest, lowest-quality downsampling (no interpolation)
    reduced_frame = cv2.resize(gray, (160, 120))

    if not ret:
        print("No more stream")
        break

        # Optionally compress with JPEG (further reduce size)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]  # Quality: 0-100 (lower = more compression)
    _, compressed_frame = cv2.imencode('.jpg', reduced_frame, encode_param)

    # Serialize the compressed frame using pickle
    data = pickle.dumps(compressed_frame)
    size = struct.pack("Q", len(data))  # Pack size as 8-byte unsigned long long

    # Send frame size and data
    client_socket.sendall(size + data)

    # Display the frame (optional)
    cv2.imshow('Reduced Video Stream', reduced_frame)

    # Quit on 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and close the socket
stream.release()
client_socket.close()
cv2.destroyAllWindows()
