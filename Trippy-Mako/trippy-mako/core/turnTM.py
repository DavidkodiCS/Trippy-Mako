import struct
import os
import socket

## Message Builders
def build_alloc():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x0003
    MAGIC_COOKIE = 0x2112A442
    TRANSACTION_ID = os.urandom(12)

    #Allocate Requires REQUESTED-TRANSPORT
    REQUESTED_TRANSPORT_TYPE = 0x0019
    REQUESTED_TRANSPORT_LENGTH = 4
    UDP_TRANSPORT = 0x11
    RESERVED = 0x00

    requested_transport = struct.pack(
        "!HHBB2x",
        REQUESTED_TRANSPORT_TYPE,
        REQUESTED_TRANSPORT_LENGTH,
        UDP_TRANSPORT,
        RESERVED
    )

    mLen = len(requested_transport)

    # LIFETIME_ATTR_TYPE = 0x000D
    # lifetime_value = 3600  # Lifetime in seconds

    # lifetime_attr = struct.pack(
    #     "!HHI",
    #     LIFETIME_ATTR_TYPE,
    #     4,
    #     lifetime_value
    # )

    # mLen += len(lifetime_attr)

    # Pack the header (Type, Length, Magic Cookie, Transaction ID)
    header = struct.pack(
        STUN_HEADER_FORMAT,  # Network byte order: 2 bytes, 2 bytes, 4 bytes, 12 bytes
        MESSAGE_TYPE,  # Message type
        mLen,         # Message length
        MAGIC_COOKIE,      # Magic cookie
        TRANSACTION_ID          # Transaction ID
    )

    alloc_packet = header + requested_transport
    return alloc_packet

def build_refresh():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x004
    MAGIC_COOKIE = 0x2112A442
    TRANSACTION_ID = os.urandom(12)

    # Pack the header (Type, Length, Magic Cookie, Transaction ID)
    header = struct.pack(
        STUN_HEADER_FORMAT,  # Network byte order: 2 bytes, 2 bytes, 4 bytes, 12 bytes
        MESSAGE_TYPE,  # Message type
        0,         # Message length
        MAGIC_COOKIE,      # Magic cookie
        TRANSACTION_ID          # Transaction ID
    )

    alloc_packet = header
    return alloc_packet

def build_send():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x006
    MAGIC_COOKIE = 0x2112A442
    TRANSACTION_ID = os.urandom(12)

def build_data():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x007
    MAGIC_COOKIE = 0x2112A442
    TRANSACTION_ID = os.urandom(12)

def build_createPerm():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x008
    MAGIC_COOKIE = 0x2112A442
    TRANSACTION_ID = os.urandom(12)

def build_channelBind():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x009
    MAGIC_COOKIE = 0x2112A442
    TRANSACTION_ID = os.urandom(12)

#Send Create Allocate
def sendAllocation(ip, port):
    turn_server = ip                          # TURN server's IP
    turn_port = int(port)        # Default TURN port most likely
    alloc_packet = build_alloc()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # Set a timeout for the response (5 seconds)
    
    try:
        # Send the Allocate packet to the TURN server
        print(f"Sending packet to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, (turn_server, turn_port))
        
        # Receive the response from the TURN server
        response, addr = sock.recvfrom(4096)  # 4096 bytes buffer size
        print(f"Received response from {addr}")

        if response:
            print("Response (hex):", response.hex())
            readServerResponse(response)

    except socket.timeout:
        print("No response received (timeout).")
    except Exception as e:
        print(f"Error: {e}")

    finally:
            sock.close()

##Refresh
def sendRefresh(self):
    refresh = build_refresh()
    
## Human Readable Server Responses ##
def readServerResponse(response):
    print(len(response))
    
    msg_type, msg_length, magic_cookie, transaction_id = struct.unpack("!HHI12s", response[:20])
    print(f"MSG_TYPE: {msg_type}")
    print(f"MSG_LENGTH: {msg_length}")
    print(f"MAGIC_COOKIE: {magic_cookie}")
    print(f"TRANSACTION_ID: {transaction_id}")
    
    response = response[20:]
    
    attr_type, attr_length, family, xor_port_ip = struct.unpack_from("!HHH4s", response[:8], 20)
    print(f"MSG_TYPE: {msg_type}")
    print(f"MSG_LENGTH: {msg_length}")
    print(f"MAGIC_COOKIE: {magic_cookie}")
    print(f"TRANSACTION_ID: {transaction_id}")
    
    
##MAIN DEBUGGING
if __name__ == "__main__":
    import turnTM
    turn_server = "127.0.0.1"  # Replace with your TURN server's IP or domain
    turn_port = 5349           # Default TURN port
    alloc_packet = build_alloc()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # Set a timeout for the response (5 seconds)
    
    try:
        # Send the Allocate packet to the TURN server
        print(f"Sending packet to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, (turn_server, turn_port))
        
        # Receive the response from the TURN server
        response, addr = sock.recvfrom(4096)  # 4096 bytes buffer size
        print(f"Received response from {addr}")

        if response:
            print("Response (hex):", response.hex())

    except socket.timeout:
        print("No response received (timeout).")
    except Exception as e:
        print(f"Error: {e}")

    finally:
            sock.close()