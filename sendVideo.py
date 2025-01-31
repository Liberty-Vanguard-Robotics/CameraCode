# import socket
# import cv2
# import pickle
# import struct

# # Open the default camera (index 0)
# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print("Error: Cannot access the camera.")
#     exit()

# while True:
#     # Capture a frame
#     ret, frame = cap.read()
    
#     if not ret:
#         print("Error: Cannot read frame from the camera.")
#         break
    
#     # Display the frame
#     cv2.imshow('Camera', frame)
    
#     # Break loop on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the camera and close the window
# cap.release()
# cv2.destroyAllWindows()

import depthai as dai
import numpy as np
import socket
import cv2
import pickle
import struct

# Function to send frame to the server
def send_frame(frame, client_socket):
    _, frame_encoded = cv2.imencode('.jpg', frame)  # Compress frame to JPEG
    data = pickle.dumps(frame_encoded)  # Serialize the compressed frame

    # Send message length first, then data
    client_socket.sendall(struct.pack("!Q", len(data)) + data)

# Function to receive command from the server
def receive_command(client_socket):
    # First, receive the message length
    data = b""
    while len(data) < struct.calcsize("L"):
        data += client_socket.recv(4096)
    msg_size = struct.unpack("L", data)[0]

    # Receive the actual command data
    data = b""
    while len(data) < msg_size:
        data += client_socket.recv(4096)

    # Deserialize the command data
    command = pickle.loads(data)
    return command

def get_frame(queue):
    frame = queue.get()
    return frame.getCvFrame()

if __name__ == '__main__':

    # Create pipeline for DepthAI
    pipeline = dai.Pipeline()

    # Set up left and right Cameras
    mono_left = pipeline.createMonoCamera()
    mono_left.setBoardSocket(dai.CameraBoardSocket.CAM_B)
    mono_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

    mono_right = pipeline.createMonoCamera()
    mono_right.setBoardSocket(dai.CameraBoardSocket.CAM_C)
    mono_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

    stereo = pipeline.createStereoDepth()
    stereo.setLeftRightCheck(True)
    mono_left.out.link(stereo.left)
    mono_right.out.link(stereo.right)

    # Set up XLink outputs
    xout_depth = pipeline.createXLinkOut()
    xout_depth.setStreamName("depth")
    stereo.disparity.link(xout_depth.input)

    xout_rect_left = pipeline.createXLinkOut()
    xout_rect_left.setStreamName("rectLeft")
    stereo.rectifiedLeft.link(xout_rect_left.input)

    xout_rect_right = pipeline.createXLinkOut()
    xout_rect_right.setStreamName("rectRight")
    stereo.rectifiedRight.link(xout_rect_right.input)

    # Setup socket to connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.207', 65432))  # Use the server's IP address

    with dai.Device(pipeline) as device:
        # Get output queues
        rect_left_queue = device.getOutputQueue(name="rectLeft", maxSize=1, blocking=False)
        rect_right_queue = device.getOutputQueue(name="rectRight", maxSize=1, blocking=False)

        while True:
            # Get frames from the output queues
            left_frame = get_frame(rect_left_queue)
            right_frame = get_frame(rect_right_queue)

            # Send left frame (or combine them as necessary) to the server
            im_out = left_frame
            im_out = cv2.cvtColor(im_out, cv2.COLOR_GRAY2RGB)

            # Send the frame to the server
            send_frame(im_out, client_socket)

            # Check for commands from the server
            command = receive_command(client_socket)
            if command == 'pause':
                print("Received pause command from server")
                cv2.waitKey(0)  # Pause until a key is pressed
            elif command == 'resume':
                print("Received resume command from server")

            # Display the frames locally (optional)
            cv2.imshow("Stereo Pair", im_out)

            # Quit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Close the socket and window
    client_socket.close()
    cv2.destroyAllWindows()

