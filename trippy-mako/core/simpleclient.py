import socket
import struct

# TURN server details
TURN_SERVER = "35.168.13.177"
TURN_PORT = 3478

# Authentication details (adjust for your server setup)
#USERNAME = "your-username"
#PASSWORD = "your-credential"

# Creates a TURN binding request header.
# The first two bytes are the message type, Binding Request
# the second two bytes are the length of the message
# Return: bytes that contain an inital binding request from client to server
def create_binding_request():
    # The TURN Binding Request Message Format
    # Message type = 0x0001 (Binding Request)
    message_type = 0x0001
    length = 0x00  # Will be updated later
    transaction_id = b'\x00' * 12  # Random 12-byte transaction ID
    
    # Construct the Binding Request message
    header = struct.pack("!HH", message_type, length) + transaction_id
    return header

def send_binding_request():
    # Create the socket and bind to the server
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(10)  # 10 seconds timeout
        binding_request = create_binding_request()
        sock.sendto(binding_request, (TURN_SERVER, TURN_PORT))
        print(f"Sent Binding Request to {TURN_SERVER}:{TURN_PORT}")
        
        # Receive response from the server
        response, addr = sock.recvfrom(1024)
        print(f"Received response from {addr}")
        print(f"Response: {response}")
        # Handle the response (parse and extract relay address or errors)

send_binding_request()
