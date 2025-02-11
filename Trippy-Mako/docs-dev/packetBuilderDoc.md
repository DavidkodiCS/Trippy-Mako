# Packet Builder Documentation

## Imports
1. **os** -> Used to create the transaction id, which is apart of every STUN message
2. **struct** -> Used to easily build packets (STUN Headers, TURN Messages, Attributes)

## Messages vs. Attributes
- **Messages:** Types of packets that are being sent to the TURN server
- **Attributes:** Special pieces of data appended to messages that often contain important information such as ip addresses, ports, data, connection lifetime, etc.

## STUN/TURN Messages

### Build_alloc() -> Allocation to TURN server
Build_alloc() returns a byte object that contains a STUN header and REQUESTED-TRANSPOT

- STUN HEADER: Required for all messages to the TURN server. 
Magic_cookie: Used to make identifing STUN from other network protocols easier.
Transaction ID: Helps the Turn Server keep track of requests/responses from clients

- REQUESTED-TRANSPORT Attribute: Client telling the TURN server that it wants to make establish a connection (the Hello)
```
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
```
### Build_refresh() -> Refresh Connection with TURN Server
Build_refresh() returns a byte object that contains a STUN header. This packet is essentially an "I'm still here" message to the TURN server.

```
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
```

### Build_kill_refresh() -> Refresh with a Lifetime of 0
Build_kill_refresh() returns a byte object that contains a STUN header and a Lifetime attribute with a value of 0.

- LIFETIME Attribute: STUN/TURN attribute
Sets the lifetime of the allocation to 0, killing the connection
```
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
```
### Build_createPerm(ip, port) -> Create Permission to connect to peer
Build_createPerm() returns a byte object that contains a STUN header and an XOR_PEER_ADDRESS attribute.

- XOR_PEER_ADDRESS Attribute: This attribute contains the XOR'd port and ip address of a peer that the client wants to talk to. It is necessary to xor the port and ip address with the STUN MAGIC_COOKIE. This is done to provide a basic protection against eavesdroppers. The magic_cookie is openly known and XOR can be reversed so this is not a great security mechanism. 

```  
def build_createPerm(ip, port):
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
```

### Build_send_indication(ip, port, payload) -> Sending a payload to the peer
Build_send_indication(ip, port, payload) returns a byte object that contains a STUN header, XOR_PEER_ADDRESS attribute, and DATA attribute.

- DATA Attribute: Contains the payload and its length. Thinking about the principle of encapsulation the data could be within other layers for additional security(**WIP**).
```
def build_send_indication(ip, port, payload):
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
    
    ## Data Attribute
    DATA_ATTRIBUTE_TYPE = 0x0013  # Attribute type for DATA
    data_length = len(payload)
    data_attribute = struct.pack("!HH", DATA_ATTRIBUTE_TYPE, data_length) + payload.encode('utf-8')
    
    
    STUN_HEADER_FORMAT = "!HHI12s"
    MESSAGE_TYPE = 0x0011
    TRANSACTION_ID = os.urandom(12)
    
    # Pack the header (Type, Length, Magic Cookie, Transaction ID)
    header = struct.pack(
        STUN_HEADER_FORMAT,  # Network byte order: 2 bytes, 2 bytes, 4 bytes, 12 bytes
        MESSAGE_TYPE,  # Message type
        xor_message_length + data_length,         # Message length
        MAGIC_COOKIE,      # Magic cookie
        TRANSACTION_ID          # Transaction ID
    )
    
    return header + xor_peer_address + data_attribute
```