import socket
import packetBuilder    


turn_server = "54.234.196.215"             # TURN server's IP
turn_port = int(3478)        # Default TURN port most likely
TURN_SERVER = tuple([turn_server, int(turn_port)])
alloc_packet = packetBuilder.build_alloc()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)  # Set a timeout for the response (5 seconds)

try:
    # Send the Allocate packet to the TURN server
    print(f"Sending packet to {turn_server}:{turn_port}")
    sock.sendto(alloc_packet, TURN_SERVER)

    ## Receive the response from the TURN server
    response, addr = sock.recvfrom(4096)  # 4096 bytes buffer size
    print(f"Received response from {addr}")

    if response:
        print("Response (hex):", response.hex())
    #     read_server_response(response)

except socket.timeout:
    print("No response received (timeout).")
except Exception as e:
    print(f"Error: {e}")  