import os
import struct
import socket

# -----------------------------
# Trippy-Mako Packet Builder
# -----------------------------
MAGIC_COOKIE = 0x2112A442

def build_stun_header(MESSAGE_TYPE, MESSAGE_LENGTH):
    STUN_HEADER_FORMAT = "!HHI12s"
    TRANSACTION_ID = os.urandom(12)
    
    header = struct.pack(
        STUN_HEADER_FORMAT,
        MESSAGE_TYPE,
        MESSAGE_LENGTH,
        MAGIC_COOKIE,
        TRANSACTION_ID
    )
    
    return header

# -----------------------------
# Build Allocate Request Packet
# -----------------------------
def build_alloc():
    MESSAGE_TYPE = 0x003

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

    return build_stun_header(MESSAGE_TYPE, message_length) + requested_transport

# ----------------------------
# Build Refresh Request Packet
# ----------------------------
def build_refresh():
    MESSAGE_TYPE = 0x004

    return build_stun_header(MESSAGE_TYPE, 0)

# ----------------------------------------------------
# Build Refresh Request with Lifetime 0 (Deallocation)
# ----------------------------------------------------
def build_kill_refresh():
    MESSAGE_TYPE = 0x004

    # Lifetime Attribute (Set to 0 for deallocation)
    lifetime_attr = struct.pack("!HHI", 0x000D, 4, 0)
    message_length = len(lifetime_attr)

    return build_stun_header(MESSAGE_TYPE, message_length) + lifetime_attr

# -------------------------------
# Build Create Permission Request
# -------------------------------
def build_createPerm(ip, port):
    MESSAGE_TYPE = 0x008  # CreatePermission Request

    # XOR-Peer-Address Attribute
    xor_port = port ^ (MAGIC_COOKIE >> 16)
    xor_ip_bytes = bytes([
        b ^ ((MAGIC_COOKIE >> (8 * (3 - i))) & 0xFF)
        for i, b in enumerate(socket.inet_aton(ip))
    ])

    xor_peer_address = struct.pack("!HHBBH4s",
        0x0012,  # Attribute Type (XOR-PEER-ADDRESS)
        8,       # Length
        0,       # Reserved
        0x01,    # Family (IPv4)
        xor_port,
        xor_ip_bytes
    )

    message_length = len(xor_peer_address)

    return build_stun_header(MESSAGE_TYPE, message_length) + xor_peer_address

# ----------------------------
# Build Send Indication Packet - NOT USED
# ----------------------------
def build_send_indication(ip, port, payload):
    MESSAGE_TYPE = 0x0016  #Send Indication Message

    # XOR-Peer-Address Attribute
    xor_port = port ^ (MAGIC_COOKIE >> 16)
    xor_ip_bytes = bytes([
        b ^ ((MAGIC_COOKIE >> (8 * (3 - i))) & 0xFF)
        for i, b in enumerate(socket.inet_aton(ip))
    ])

    xor_peer_address = struct.pack("!HHBBH4s",
        0x0012,  # XOR-PEER-ADDRESS
        8,       # Length
        0,       # Reserved
        0x01,    # Family (IPv4)
        xor_port,
        xor_ip_bytes
    )

    # Data Attribute
    data = payload.encode('utf-8')
    data_length_padded = (len(data) + 3) & ~3
    padding = b"\x00" * (data_length_padded - len(data))
    data_attribute = struct.pack("!HH", 0x0013, len(data)) + data + padding

    # Length
    message_length = len(xor_peer_address) + len(data_attribute)

    return build_stun_header(MESSAGE_TYPE, message_length) + xor_peer_address + data_attribute


# --------------------------
# Build Channel Bind Request
# --------------------------
def build_channelBind(ip, port, channel_number):
    MESSAGE_TYPE = 0x009  # Channel Bind Request

    # XOR-Peer-Address Attribute
    xor_port = port ^ (MAGIC_COOKIE >> 16)
    xor_ip_bytes = bytes([
        b ^ ((MAGIC_COOKIE >> (8 * (3 - i))) & 0xFF)
        for i, b in enumerate(socket.inet_aton(ip))
    ])

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

    # Length
    message_length = len(xor_peer_address) + len(channel_attribute)

    return build_stun_header(MESSAGE_TYPE, message_length) + xor_peer_address + channel_attribute

# --------------------------
# Build Channel Data Message
# --------------------------
def build_channelData(channel_number, data):
    data_bytes = data.encode('utf-8')
    length = len(data_bytes)

    # ChannelData Header: Channel Number (16-bit) + Length (16-bit)
    header = struct.pack("!HH", channel_number, length)

    return header + data_bytes

# -----------------------
# Build STUN Bind Request - NOT USED
# -----------------------
def build_stun_bind():
    MESSAGE_TYPE = 0x0001  # STUN Bind Request

    return build_stun_header(MESSAGE_TYPE, 0)