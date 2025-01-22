# ########################################
# # This runs on the the computer we have
# ########################################

# import depthai as dai
# import numpy as np
# import socket
# import cv2
# import pickle
# import struct

# def receive_video():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(('192.168.168.xxx', 65432)) # replace address
#     server_socket.listen(1)
#     print("Server listening on port 65432...")

#     conn, addr = server_socket.accept()
#     print(f'Connection from {addr} established.')

#     data = b""
#     payload_size = struct.calcsize("L")
#     while True:
#     # Retrieve message size first
#         while len(data) < payload_size:
#             packet = conn.recv(4096)
#             if not packet:
#                 break
#             data += packet


#         packed_msg_size = data[:payload_size]
#         data = data[payload_size:]
#         msg_size = struct.unpack("L", packed_msg_size)[0]

#         # Retrieve all data based on message size
#         while len(data) < msg_size:
#             data += conn.recv(4096)

#         frame_data = data[:msg_size]
#         data = data[msg_size:]

#         # Deserialize and decode the frame
#         frame = pickle.loads(frame_data)
#         frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

#         cv2.imshow("Stereo Pair", frame)

#     conn.close()
#     server_socket.close()
#     cv2.destroyAllWindows()

# receive_video()




import socket
import pickle
import cv2
import struct

# Server setup to receive video
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))  # Bind to all interfaces (0.0.0.0) and port 65432
server_socket.listen(1)  # Wait for incoming connections

print("Server is waiting for connection...")
client_socket, addr = server_socket.accept()  # Accept the connection
print(f"Connection from {addr} established!")

# Receiving video
while True:
    # First, receive the message length
    data = b""
    while len(data) < struct.calcsize("L"):
        data += client_socket.recv(4096)
    msg_size = struct.unpack("L", data)[0]

    # Receive the actual frame data
    data = b""
    while len(data) < msg_size:
        data += client_socket.recv(4096)

    # Deserialize the frame data
    frame_data = pickle.loads(data)
    frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)  # Decode the JPEG frame

    # Display the frame
    if frame is not None:
        cv2.imshow("Received Video", frame)

    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the socket and window
client_socket.close()
server_socket.close()
cv2.destroyAllWindows()
