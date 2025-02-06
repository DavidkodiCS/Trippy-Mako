import os
import asyncio
import socket
import struct
import time

## MESSAGE TYPES
STUN_MESSAGE_TYPES = {
    0x001: "Binding Request",
    0x101: "Binding Response",
    0x111: "Binding Error Response",
    0x003: "Allocate Request",
    0x103: "Allocate Response",
    0x113: "Allocate Error Response",
    0x004: "Refresh Request",
    0x104: "Refresh Response",
    0x114: "Refresh Error Response",
    0x016: "Send Indication",
    0x116: "Data Indication",
    0x008: "CreatePermission Request",
    0x108: "CreatePermission Response",
    0x118: "CreatePermission Error Response",
    0x009: "ChannelBind Request",
    0x109: "ChannelBind Response",
    0x119: "ChannelBind Error Response",
}


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

def build_kill_refresh():
        ##Lifetime of 0 to deallocate
        lifetime_attr = struct.pack("!HHI", 0x000D, 4, 0)  
        attr_len = len(lifetime_attr)
    
        STUN_HEADER_FORMAT = "!HHI12s"
        MESSAGE_TYPE = 0x004
        MAGIC_COOKIE = 0x2112A442
        TRANSACTION_ID = os.urandom(12)

        # Pack the header (Type, Length, Magic Cookie, Transaction ID)
        header = struct.pack(
            STUN_HEADER_FORMAT,  # Network byte order: 2 bytes, 2 bytes, 4 bytes, 12 bytes
            MESSAGE_TYPE,  # Message type
            attr_len,         # Message length
            MAGIC_COOKIE,      # Magic cookie
            TRANSACTION_ID          # Transaction ID
        )

        dealloc_packet = header + lifetime_attr
        return dealloc_packet

def build_send_indication(xor_peer_address, payload):
    ## XOR-Peer-Address Attribute
    
    
    ## Data Attribute
    
    
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x006
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
    
    return header

def build_data_indication():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x007
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
    
    return header

def build_createPerm(ip, port):
    MAGIC_COOKIE = 0x2112A442
    ## XOR PORT + MAGIC COOKIE
    xor_port = port ^ (MAGIC_COOKIE >> 16)
    
    ## IP address to Bytes
    ip_bytes = bytes([ip[i] ^ ((MAGIC_COOKIE >> (8 * (3 - i))) & 0xFF) for i in range(4)])
    
    MESSAGE_TYPE = 0x0012
    
    xor_peer_address = struct.pack("!HHBBH4s", 
        MESSAGE_TYPE,  # Attribute Type (XOR-PEER-ADDRESS)
        8,       # Length
        0,       # Reserved
        0x01,    # Family (IPv4)
        xor_port,  # XOR'ed Port
        ip_bytes)  # XOR'ed IP Address
    
    xor_message_length = len(xor_peer_address)
    
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x008
    #MAGIC COOKIE
    TRANSACTION_ID = os.urandom(12)
    
    # Pack the header (Type, Length, Magic Cookie, Transaction ID)
    header = struct.pack(
        STUN_HEADER_FORMAT,  # Network byte order: 2 bytes, 2 bytes, 4 bytes, 12 bytes
        MESSAGE_TYPE,  # Message type
        xor_message_length,         # Message length
        MAGIC_COOKIE,      # Magic cookie
        TRANSACTION_ID          # Transaction ID
    )
    
    return header + xor_peer_address

def build_channelBind():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x009
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
    
    return header
    
## Human Readable Server Responses ##
def readServerResponse(response):    
    msg_type, msg_length, magic_cookie, transaction_id = struct.unpack_from("!HHI12s", response, 0)
    print(f"MSG_TYPE: {STUN_MESSAGE_TYPES.get(msg_type)}")
    print(f"MSG_LENGTH: {msg_length}")
    print(f"MAGIC_COOKIE: {hex(magic_cookie)}")
    print(f"TRANSACTION_ID: {transaction_id.hex()}")
    
    offset = 20  # Start of attributes

    # Parse Attributes
    while offset < len(response):
        attr_type, attr_length = struct.unpack_from("!HH", response, offset)
        offset += 4  # Move past type and length

        attr_value = response[offset : offset + attr_length]
        offset += attr_length  # Move past value

        if attr_type == 0x000D:  # LIFETIME
            lifetime = struct.unpack("!I", attr_value)[0]
            print(f"Lifetime\n\tValue: {lifetime} seconds")

        elif attr_type == 0x0020:  # XOR-MAPPED-ADDRESS
            family, xor_port = struct.unpack("!HH", attr_value[:4])
            #MAGIC COOKIE
            xor_ip = struct.unpack("!I", attr_value[4:])[0] ^ 0x2112A442
            ip_addr = ".".join(map(str, xor_ip.to_bytes(4, 'big')))
            port = xor_port ^ 0x2112
            print(f"XOR-MAPPED-ADDRESS\n\tIP: {ip_addr}\n\tPORT: {port}")

        elif attr_type == 0x0008:  # RESERVED ADDRESS (another XOR-MAPPED-ADDRESS)
            family, xor_port = struct.unpack("!HH", attr_value[:4])
            xor_ip = struct.unpack("!I", attr_value[4:])[0] ^ 0x2112A442
            ip_addr = ".".join(map(str, xor_ip.to_bytes(4, 'big')))
            port = xor_port ^ 0x2112
            print(f"Reserved XOR-MAPPED-ADDRESS\n\tIP: {ip_addr}\n\tPORT: {port}")

        elif attr_type == 0x8022:  # SOFTWARE
            software_version = attr_value.decode(errors="ignore")
            print(f"Software\n\tValue: {software_version}")

        elif attr_type == 0x8028:  # FINGERPRINT
            fingerprint = struct.unpack("!I", attr_value)[0]
            print(f"Fingerprint\n\tValue: {fingerprint}")
        
# Helper function to XOR decode addresses
def xor_decode(value, key):
    return bytes(b1 ^ b2 for b1, b2 in zip(value, key))

##Send refresh async
async def send_refresh(sock, TURN_SERVER):
   while True:
        refresh = build_refresh()
        sock.sendto(refresh, TURN_SERVER)
        print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
        
        await asyncio.sleep(300)  # Wait 300 seconds before sending again
        
    

## Start client ##
async def start_client(ip, port):
    turn_server = ip             # TURN server's IP
    turn_port = int(port)        # Default TURN port most likely
    TURN_SERVER = tuple([turn_server, int(turn_port)])
    alloc_packet = build_alloc()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # Set a timeout for the response (5 seconds)
    
    try:
        # Send the Allocate packet to the TURN server
        print(f"Sending packet to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, TURN_SERVER)
        
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
            
    ## Maintain connection with refresh packets
    asyncio.create_task(send_refresh(sock, TURN_SERVER))
    
    print("Waiting...")
    await asyncio.sleep(10)
    kill = build_kill_refresh()
    sock.sendto(kill, TURN_SERVER)
        
##MAIN DEBUGGING
# if __name__ == "__main__":
#     import turnTM
#     turn_server = "127.0.0.1"  # Replace with your TURN server's IP or domain
#     turn_port = 5349           # Default TURN port
#     alloc_packet = build_alloc()

#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.settimeout(5)  # Set a timeout for the response (5 seconds)
    
#     try:
#         # Send the Allocate packet to the TURN server
#         print(f"Sending packet to {turn_server}:{turn_port}")
#         sock.sendto(alloc_packet, (turn_server, turn_port))
        
#         # Receive the response from the TURN server
#         response, addr = sock.recvfrom(4096)  # 4096 bytes buffer size
#         print(f"Received response from {addr}")

#         if response:
#             print("Response (hex):", response.hex())

#     except socket.timeout:
#         print("No response received (timeout).")
#     except Exception as e:
#         print(f"Error: {e}")

#     finally:
#             sock.close()