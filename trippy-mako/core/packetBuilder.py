## Message Builders
import os
import struct
import socket

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

    refresh_packet = header
    return refresh_packet

## Sets the lifetime of the allocation to 0, killing the connection
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
    
import struct
import os
import socket

def build_createPerm(ip, port):
    MAGIC_COOKIE = 0x2112A442
    MESSAGE_TYPE = 0x0008  # CreatePermission Request
    
    # XOR-Peer-Address Attribute
    xor_port = port ^ (MAGIC_COOKIE & 0xFFFF)  # Corrected XOR operation
    ip_bytes = socket.inet_aton(ip)
    xor_ip_bytes = bytes([b ^ ((MAGIC_COOKIE >> (8 * (3 - i))) & 0xFF) for i, b in enumerate(ip_bytes)])

    xor_peer_address = struct.pack("!HHBBH4s", 
        0x0012,  # Attribute Type (XOR-PEER-ADDRESS)
        8,       # Length
        0,       # Reserved
        0x01,    # Family (IPv4)
        xor_port,  # XOR'ed Port
        xor_ip_bytes)  # XOR'ed IP Address

    # Corrected STUN header length calculation
    TRANSACTION_ID = os.urandom(12)
    message_length = len(xor_peer_address)
    
    stun_header = struct.pack("!HHI12s", MESSAGE_TYPE, message_length, MAGIC_COOKIE, TRANSACTION_ID)

    return stun_header + xor_peer_address


def build_send_indication(ip, port, payload):
    MAGIC_COOKIE = 0x2112A442
    MESSAGE_TYPE = 0x0011  # Send Indication
    
    ## XOR-Peer-Address Attribute
    xor_port = port ^ (MAGIC_COOKIE & 0xFFFF)  # Correct XOR operation
    ip_bytes = socket.inet_aton(ip)
    xor_ip_bytes = bytes([b ^ ((MAGIC_COOKIE >> (8 * (3 - i))) & 0xFF) for i, b in enumerate(ip_bytes)])

    xor_peer_address = struct.pack("!HHBBH4s", 
        0x0012,  # Attribute Type (XOR-PEER-ADDRESS)
        8,       # Length
        0,       # Reserved
        0x01,    # Family (IPv4)
        xor_port,  # XOR'ed Port
        xor_ip_bytes)  # XOR'ed IP Address

    ## Data Attribute (with padding)
    DATA_ATTRIBUTE_TYPE = 0x0013
    data = payload.encode('utf-8')
    data_length = len(data)
    data_length_padded = (data_length + 3) & ~3  # Ensure 4-byte alignment
    padding = b"\x00" * (data_length_padded - data_length)
    data_attribute = struct.pack("!HH", DATA_ATTRIBUTE_TYPE, data_length) + data + padding

    ## STUN Header
    TRANSACTION_ID = os.urandom(12)
    message_length = len(xor_peer_address) + len(data_attribute)  # Corrected length calculation
    stun_header = struct.pack("!HHI12s", MESSAGE_TYPE, message_length, MAGIC_COOKIE, TRANSACTION_ID)

    return stun_header + xor_peer_address + data_attribute

## Channel Bind ##
def build_channelBind(ip, port, channel_number):
    ## XOR-Peer-Address Attribute
    MAGIC_COOKIE = 0x2112A442
    ## XOR PORT + MAGIC COOKIE
    xor_port = port ^ (MAGIC_COOKIE >> 16)
    
    ## IP address to Bytes
    ip = socket.inet_aton(ip)
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
    
    ## Channel Attribute
    CHANNEL_NUMBER_ATTR_TYPE = 0x000C
    channel_attribute = struct.pack("!HHH2s",
        CHANNEL_NUMBER_ATTR_TYPE,  # Attribute Type
        4,  # Length (Always 4 bytes)
        channel_number,  # Assigned Channel Number (0x4000 - 0x7FFF)
        b'\x00\x00'  # Reserved (2 bytes)
    )
    
    channel_attribute_length = len(channel_attribute)
    
    
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x009
    TRANSACTION_ID = os.urandom(12)
    
    # Pack the header (Type, Length, Magic Cookie, Transaction ID)
    header = struct.pack(
        STUN_HEADER_FORMAT,  # Network byte order: 2 bytes, 2 bytes, 4 bytes, 12 bytes
        MESSAGE_TYPE,  # Message type
        xor_message_length + channel_attribute_length,         # Message length
        MAGIC_COOKIE,      # Magic cookie
        TRANSACTION_ID          # Transaction ID
    )
    
    return header + xor_peer_address + channel_attribute

## Channel Data Message ##
def build_channelData(data, CHANNEL_NUMBER):
    CHANNEL_HEADER_FORMAT = "!HH"
    
    header = struct.pack(
        CHANNEL_HEADER_FORMAT,
        CHANNEL_NUMBER,
        len(data)
    )
    
    return header + data.encode('utf-8')