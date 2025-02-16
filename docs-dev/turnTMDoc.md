# TurnTM Documentation

## Imports

1. asyncio: Used to establish coroutines and tasks to be completeled in parallel to the main event loop
2. socket: Used to establish network communication to the TURN server
3. struct: Used to unpack messages from the TURN server in readServerResponse(response)
4. time: Used to print out time when a message is sent
5. packetBuilder: Used to build STUN/TURN packets

## Driver Code for TURN Implementation

### MESSAGE TYPES

```
STUN_MESSAGE_TYPES = {
    0x0001: "Binding Request",
    0x0101: "Binding Success Response",
    0x0111: "Binding Error Response",

    0x0003: "Allocate Request",
    0x0103: "Allocate Success Response",
    0x0113: "Allocate Error Response",

    0x0004: "Refresh Request",
    0x0104: "Refresh Success Response",
    0x0114: "Refresh Error Response",

    0x0006: "Send Indication",
    0x0017: "Data Indication",

    0x0008: "CreatePermission Request",
    0x0108: "CreatePermission Success Response",
    0x0118: "CreatePermission Error Response",

    0x0009: "ChannelBind Request",
    0x0109: "ChannelBind Success Response",
    0x0119: "ChannelBind Error Response",
}
```

## Client Helper Functions

### Send_refresh(sock, TURN_SERVER)

This function takes the socket and the IP/PORT tuple as parameters. Send_refresh is called as a asyncio task in each of the clients in order to asynchronously run in parallel to the main loop.

Once made a task, send_refresh will build a refresh packet, send the refresh to the TURN Server, receive the server's response, print that response using readServerResponse, and then wait 300 seconds before executing again.

A refresh must be sent to the TURN server before the allocation's lifetime expires in order to maintain the connection between the client and TURN server. The standard lifetime for an allocation is 600 seconds so in our implementation a refresh is sent every 300 seconds to ensure the connection stays alive.

```
async def send_refresh(sock, TURN_SERVER):
   while True:
        refresh = packetBuilder.build_refresh()
        sock.sendto(refresh, TURN_SERVER)
        print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")

        response, addr = sock.recvfrom(4096)  # 4096 bytes buffer size
        print(f"Received response from {addr}")
        if response:
            print("Response (hex):", response.hex())
            readServerResponse(response)


        await asyncio.sleep(300) # Wait 300 seconds before sending again
```

### Read_server_response(response)

read_server_response takes a byte response from the TURN server as the parameter and prints out the plaintext version of this response.

Every message will begin with the STUN header which always makes up the first 20 bytes of the packet. 

The offset, beginning at 20, will increment based on the next attribute's size until the offset reaches the total length of the response. The first two bytes of each attribute will be its type and length which is used to determine how it should be parsed and how much the offset should be increased by.

Based on the attribute type hex values the case statements will perform the correct parsing for that specific attribute.

The cycle will continue until the message is fully parsed. 

```
def read_server_response(response):    
    msg_type, msg_length, magic_cookie, transaction_id = struct.unpack_from("!HHI12s", response, 0)
    print(f"MSG_TYPE: {STUN_MESSAGE_TYPES.get(msg_type)}")
    print(f"MSG_LENGTH: {msg_length}")
    print(f"MAGIC_COOKIE: {hex(magic_cookie)}")
    print(f"TRANSACTION_ID: {transaction_id.hex()}")
    
    offset = 20  # Start of attributes

    # Parse Attributes
    while offset < len(response):
        MAGIC_COOKIE = 0x2112A442
        attr_type, attr_length = struct.unpack_from("!HH", response, offset)
        offset += 4  # Move past type and length

        attr_value = response[offset : offset + attr_length]
        offset += attr_length  # Move past value

        match attr_type:
            case 0x000D: # LIFETIME
                lifetime = struct.unpack("!I", attr_value)[0]
                print(f"Lifetime\n\tValue: {lifetime} seconds")
            case 0x0020: # XOR-MAPPED-ADDRESS
                family, xor_port = struct.unpack("!HH", attr_value[:4])
                #MAGIC COOKIE
                xor_ip = struct.unpack("!I", attr_value[4:])[0] ^ MAGIC_COOKIE
                ip_addr = ".".join(map(str, xor_ip.to_bytes(4, 'big')))
                port = xor_port ^ 0x2112
                print(f"XOR-MAPPED-ADDRESS\n\tIP: {ip_addr}\n\tPORT: {port}")
            case 0x0008: # RESERVED ADDRESS (another XOR-MAPPED-ADDRESS)
                family, xor_port = struct.unpack("!HH", attr_value[:4])
                xor_ip = struct.unpack("!I", attr_value[4:])[0] ^ MAGIC_COOKIE
                ip_addr = ".".join(map(str, xor_ip.to_bytes(4, 'big')))
                port = xor_port ^ 0x2112
                print(f"Reserved XOR-MAPPED-ADDRESS\n\tIP: {ip_addr}\n\tPORT: {port}")
            case 0x8022: # SOFTWARE
                software_version = attr_value.decode(errors="ignore")
                print(f"Software\n\tValue: {software_version}")
            case 0x8028: # FINGERPRINT
                fingerprint = struct.unpack("!I", attr_value)[0]
                print(f"Fingerprint\n\tValue: {fingerprint}")
            case 0x0013: # DATA
                data = attr_value
                print(f"🔹 DATA (Received from peer):\n\t{data.hex()}") 
                print(f"\tDecoded: {data.decode()}")
            case 0x0012: # XOR-PEER-ADDRESS (PEER)
                family, xor_port = struct.unpack("!HH", attr_value[:4])
                xor_ip = struct.unpack("!I", attr_value[4:])[0] ^ 0x2112A442
                peer_ip = ".".join(map(str, xor_ip.to_bytes(4, 'big')))
                peer_port = xor_port ^ 0x2112
                print(f"🔹 XOR-PEER-ADDRESS\n\tIP: {peer_ip}\n\tPORT: {peer_port}")
```

## Client Functionality

### Start_send_client(ip, port) -> Executes Trippy-Mako SEND feature

start_send_client executes the functionality for the send feature. The user will be prompted to enter in the peer's port and ip address. This function then creates an allocation to be sent to the TURN Server using the ip and port parameters. A send_refresh task is created in order to keep the connection between the client and TURN Server alive.

Using the peer port and ip address a Create Permission packet will be created and sent to the TURN Server in order to get permission to send data to the desired peer. At this point the TURN Server will allow the client to communicate with the peer.

Finally, the user will be able to send messages, and later entire payloads, to the peer that they will receive and be able to read with read_server_response. 

```
async def start_send_client(ip, port):
    turn_server = ip             # TURN server's IP
    turn_port = int(port)        # Default TURN port most likely
    peer_ip = input("IP of Peer: ")
    peer_port = int(input("Port of peer: "))
    TURN_SERVER = tuple([turn_server, int(turn_port)])
    alloc_packet = packetBuilder.build_alloc()
    create_perm_packet = packetBuilder.build_createPerm(peer_ip, peer_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(None)  # Set a timeout for the response (5 seconds)
    
    try:
        # Send the Allocate packet to the TURN server
        print(f"Sending packet to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, TURN_SERVER)
        
        # Receive the response from the TURN server
        response, addr = sock.recvfrom(4096)  # 4096 bytes buffer size
        print(f"Received response from {addr}")

        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)
            
        # Send the Create Perm packet to the TURN server
        print(f"Sending packet to {turn_server}:{turn_port}")
        sock.sendto(create_perm_packet, TURN_SERVER)
        
        # Receive the response from the TURN server
        response, addr = sock.recvfrom(4096)  # 4096 bytes buffer size
        print(f"Received response from {addr}")

        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)

    except socket.timeout:
        print("No response received (timeout).")
    except Exception as e:
       print(f"Error: {e}")    
            
    ## Maintain connection with refresh packets
    asyncio.create_task(send_refresh(sock, TURN_SERVER))
```

### Start_listener_client(ip, port) -> Executes Trippy-Mako LISTEN feature

start_listener_client executes the functionality for the listen feature. This function creates an allocation to be sent to the TURN Server using the ip and port parameters. A send_refresh task is created in order to keep the connection between the client and TURN Server alive.

The socket timeout is set to None in order to keep the socket alive even while not receiving any data.

Finally, the listener will wait for a response from the server that hopefully contains data from a peer attempting to communicate.

```
async def start_listener_client(ip, port):
    turn_server = ip             # TURN server's IP
    turn_port = int(port)        # Default TURN port most likely
    TURN_SERVER = tuple([turn_server, int(turn_port)])
    loop = asyncio.get_event_loop()
    
    alloc_packet = packetBuilder.build_alloc()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(None)  # Set a timeout for the response (5 seconds)
    
    try:
        # Send the Allocate packet to the TURN server
        print(f"Sending packet to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, TURN_SERVER)
        
        # Receive the response from the TURN server
        response, addr = sock.recvfrom(4096)  # 4096 bytes buffer size
        print(f"Received response from {addr}")

       # Receive the response from the TURN server
        response, addr = sock.recvfrom(4096)  # 4096 bytes buffer size
        print(f"Received response from {addr}")

        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)

    except socket.timeout:
        print("No response received (timeout).")
    except Exception as e:
       print(f"Error: {e}")  
       
    ## Maintain connection with refresh packets
    asyncio.create_task(send_refresh(sock, TURN_SERVER))

    while True:
        response, addr = await loop.sock.recvfrom(sock, 4096)
        print(f"Received response from {addr}")

        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)
```