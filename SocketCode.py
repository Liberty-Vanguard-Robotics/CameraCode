import socket
import pickle

def send_data(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('192.168.168.206', 65432))

            # Serialize data to send
            serialized_data = pickle.dumps(data)

            client_socket.sendall(serialized_data)
            print("Data Sent")
    except Exception as e:
        print(f"Error: {e}")

# Directly define the data to send (instead of using test3_gather)
data_to_send = [[1, 2, 3], [4, 5, 6]]  # Example data, replace with your actual data
send_data(data_to_send)