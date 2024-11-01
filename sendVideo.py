import socket
import cv2
import pickle
import struct

def send_video():
    # Initialize camera
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera

    # Setup client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.168.2', 65432))

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # Compress frame to JPEG format
        _, frame_encoded = cv2.imencode('.jpg', frame)
        
        # Serialize the compressed frame
        data = pickle.dumps(frame_encoded)
        
        # Send message length first, then data
        client_socket.sendall(struct.pack("L", len(data)) + data)
    
    # Release the camera and close the socket
    cap.release()
    client_socket.close()

# Run the client
send_video()
