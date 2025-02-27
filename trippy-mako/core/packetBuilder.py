import os
import struct
import socket


# -----------------------------
# Trippy-Mako Packet Builder
# -----------------------------

# Build Allocate Request Packet
def build_alloc():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x0003
    MAGIC_COOKIE = 0x2112A442
    TRANSACTION_ID = os.urandom(12)

    # Requested Transport Attribute
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

    message_length = len(requested_transport)

    # STUN Header
    header = struct.pack(
        STUN_HEADER_FORMAT,
        MESSAGE_TYPE,
        message_length,
        MAGIC_COOKIE,
        TRANSACTION_ID
    )

    return header + requested_transport

# Build Refresh Request Packet
def build_refresh():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x0004
    MAGIC_COOKIE = 0x2112A442
    TRANSACTION_ID = os.urandom(12)

    # STUN Header
    header = struct.pack(
        STUN_HEADER_FORMAT,
        MESSAGE_TYPE,
        0,  # Message length (no attributes)
        MAGIC_COOKIE,
        TRANSACTION_ID
    )

    return header

# Build Refresh Request with Lifetime 0 (Deallocation)
def build_kill_refresh():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x0004
    MAGIC_COOKIE = 0x2112A442
    TRANSACTION_ID = os.urandom(12)

    # Lifetime Attribute (Set to 0 for deallocation)
    lifetime_attr = struct.pack("!HHI", 0x000D, 4, 0)
    message_length = len(lifetime_attr)

    # STUN Header
    header = struct.pack(
        STUN_HEADER_FORMAT,
        MESSAGE_TYPE,
        message_length,
        MAGIC_COOKIE,
        TRANSACTION_ID
    )

    return header + lifetime_attr

# Build Create Permission Request
def build_createPerm(ip, port):
    MAGIC_COOKIE = 0x2112A442
    MESSAGE_TYPE = 0x0008  # CreatePermission Request
    TRANSACTION_ID = os.urandom(12)

    # XOR-Peer-Address Attribute
    xor_port = port ^ (MAGIC_COOKIE & 0xFFFF)
    xor_ip_bytes = bytearray(socket.inet_aton(ip))
    for i in range(4):
        xor_ip_bytes[i] ^= (MAGIC_COOKIE >> (8 * (3 - i))) & 0xFF

    xor_peer_address = struct.pack("!HHBBH4s",
        0x0012,  # Attribute Type (XOR-PEER-ADDRESS)
        8,       # Length
        0,       # Reserved
        0x01,    # Family (IPv4)
        xor_port,
        xor_ip_bytes
    )

    message_length = len(xor_peer_address)
    stun_header = struct.pack("!HHI12s", MESSAGE_TYPE, message_length, MAGIC_COOKIE, TRANSACTION_ID)

    return stun_header + xor_peer_address

# Build Send Indication Packet
def build_send_indication(ip, port, payload):
    MAGIC_COOKIE = 0x2112A442
    MESSAGE_TYPE = 0x0011  # Send Indication
    TRANSACTION_ID = os.urandom(12)

    # XOR-Peer-Address Attribute
    xor_port = port ^ (MAGIC_COOKIE & 0xFFFF)
    xor_ip_bytes = bytearray(socket.inet_aton(ip))
    for i in range(4):
        xor_ip_bytes[i] ^= (MAGIC_COOKIE >> (8 * (3 - i))) & 0xFF

    xor_peer_address = struct.pack("!HHBBH4s",
        0x0012,  # Attribute Type (XOR-PEER-ADDRESS)
        8,       # Length
        0,       # Reserved
        0x01,    # Family (IPv4)
        xor_port,
        xor_ip_bytes
    )

    # Data Attribute
    data = payload.encode('utf-8')
    data_length_padded = (len(data) + 3) & ~3  # Ensure 4-byte alignment
    padding = b"\x00" * (data_length_padded - len(data))
    data_attribute = struct.pack("!HH", 0x0013, len(data)) + data + padding

    message_length = len(xor_peer_address) + len(data_attribute)
    stun_header = struct.pack("!HHI12s", MESSAGE_TYPE, message_length, MAGIC_COOKIE, TRANSACTION_ID)

    return stun_header + xor_peer_address + data_attribute

# Build Channel Bind Request
def build_channelBind(ip, port, channel_number):
    MAGIC_COOKIE = 0x2112A442
    MESSAGE_TYPE = 0x0009  # Channel Bind Request
    TRANSACTION_ID = os.urandom(12)

    # XOR-Peer-Address Attribute
    xor_port = port ^ (MAGIC_COOKIE >> 16)
    xor_ip_bytes = bytes([b ^ ((MAGIC_COOKIE >> (8 * (3 - i))) & 0xFF) for i, b in enumerate(socket.inet_aton(ip))])

    xor_peer_address = struct.pack("!HHBBH4s",
        0x0012,  # Attribute Type (XOR-PEER-ADDRESS)
        8,       # Length
        0,       # Reserved
        0x01,    # Family (IPv4)
        xor_port,
        xor_ip_bytes
    )

    # Channel Number Attribute
    channel_attribute = struct.pack("!HHH2s",
        0x000C,  # Attribute Type
        4,  # Length
        channel_number,  # Channel Number
        b'\x00\x00'  # Reserved
    )

    message_length = len(xor_peer_address) + len(channel_attribute)
    stun_header = struct.pack("!HHI12s", MESSAGE_TYPE, message_length, MAGIC_COOKIE, TRANSACTION_ID)

    return stun_header + xor_peer_address + channel_attribute

# Build Channel Data Message
def build_channelData(data, channel_number):
    header = struct.pack("!HH", channel_number, len(data))
    return header + data.encode('utf-8')

# Build STUN Bind Request
def build_stun_bind():
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x0001  # STUN Bind Request
    MAGIC_COOKIE = 0x2112A442
    TRANSACTION_ID = os.urandom(12)

    header = struct.pack(
        STUN_HEADER_FORMAT,
        MESSAGE_TYPE,
        0,  # No attributes
        MAGIC_COOKIE,
        TRANSACTION_ID
    )

    return header