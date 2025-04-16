import cv2
import socket
import struct
import pickle

# Set up the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 9999))  # Listen on all interfaces
server_socket.listen(1)
output_width, output_height = 640, 480
print("Waiting for connection...")

conn, addr = server_socket.accept()
print(f"Connected to {addr}")

while True:
    # Receive frame size
    packed_size = conn.recv(8)
    if not packed_size:
        break

    size = struct.unpack("Q", packed_size)[0]

    # Receive frame data
    data = b""
    while len(data) < size:
        data += conn.recv(size - len(data))
    try:
    # Deserialize the data (it was serialized using pickle)
        frame = pickle.loads(data)

    # If frame was JPEG compressed, we need to decode it
        frame = cv2.imdecode(frame, cv2.IMREAD_GRAYSCALE)  # Assuming grayscale frames
    except Exception as e:
        print(f"Frame decode error: {e}")
        continue
    
    if frame is None:
        print("Failed to decode frame.")
        break

    # Resize frame to the desired output size
    frame_resized = cv2.resize(frame, (output_width, output_height))

    # Display the frame
    cv2.imshow("Received Stream", frame_resized)

    # Quit on 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Close connections
conn.close()
server_socket.close()
cv2.destroyAllWindows()

