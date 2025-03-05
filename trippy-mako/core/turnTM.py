import random
import socket
import struct
import sys
import time
import packetBuilder
import os
import subprocess
import select

# -------------------------------------------
# Trippy-Mako TURN Client/Peer Implementation
# -------------------------------------------

## MESSAGE TYPES ##
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

# ------------------------------------
# Quick Message Feature
# ------------------------------------

# ------------------------------------
# Quick Message Client
# ------------------------------------
def start_quick_message_client(ip, port):
    turn_server = ip  # TURN server's IP
    turn_port = int(port)  # Default TURN port most likely
    TURN_SERVER = (turn_server, turn_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(None)  # No timeout
    sock.setblocking(False)  # Non-blocking socket

    # Generate a random valid channel number (RFC 5766: between 0x4000 - 0x7FFF)
    channel_number = 0x4001

    # Allocate Request
    alloc_packet = packetBuilder.build_alloc()
    print(f"Sending Allocate packet to {turn_server}:{turn_port}")
    sock.sendto(alloc_packet, TURN_SERVER)

    # Wait for a response
    ready, _, _ = select.select([sock], [], [], 5)
    if sock in ready:
        response, addr = sock.recvfrom(4096)
        print(f"Received response from {addr}")
        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)
    else:
        print("No response received from TURN server.")

    # Get Peer Information
    peer_ip = input("XOR-MAP IP of Peer: ")
    peer_port = 0

    # Create Permission Request
    create_perm_packet = packetBuilder.build_createPerm(peer_ip, peer_port)
    print(f"Sending Create Permission packet to {turn_server}:{turn_port}")
    sock.sendto(create_perm_packet, TURN_SERVER)

    # Wait for a response
    ready, _, _ = select.select([sock], [], [], 5)
    if sock in ready:
        response, addr = sock.recvfrom(4096)
        print(f"Received response from {addr}")
        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)
    else:
        print("No response received from TURN server.")

    peer_ip = input("RTA IP of Peer: ")
    peer_port = int(input("RTA PORT of Peer: "))

    # Send Channel Bind Request
    channel_bind_packet = packetBuilder.build_channelBind(peer_ip, peer_port, channel_number)
    print(f"Sending Channel Bind Request (Channel {channel_number})...")
    sock.sendto(channel_bind_packet, TURN_SERVER)

    # Wait for a response
    ready, _, _ = select.select([sock], [], [], 5)
    if sock in ready:
        response, addr = sock.recvfrom(4096)
        print(f"Received response from {addr}")
        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)
    else:
        print("No response received from TURN server.")

    # Refresh Allocation
    try:
        refresh_packet = packetBuilder.build_refresh()
        print(f"Sending Refresh packet to {turn_server}:{turn_port}")
        sock.sendto(refresh_packet, TURN_SERVER)

        # Wait for a response
        ready, _, _ = select.select([sock], [], [], 5)
        if sock in ready:
            response, addr = sock.recvfrom(4096)
            print(f"Received response from {addr}")
            if response:
                print("Response (hex):", response.hex())
                read_server_response(response)
        else:
            print("No response received from TURN server.")
    except Exception as e:
        print(f"Error: {e}")

    # Start Message Loop
    last_refresh_time = time.time()
    refresh_interval = 60  # Refresh every 1 minute

    print("Send quick messages. Enter 'q' to quit.")

    while True:
        # Calculate time until next refresh
        time_until_refresh = max(0, refresh_interval - (time.time() - last_refresh_time))

        # Check for socket activity and user input
        ready, _, _ = select.select([sock, sys.stdin], [], [], time_until_refresh)

        if sock in ready:
            try:
                response, addr = sock.recvfrom(4096)
                print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")

                if response:
                    print("Response (hex):", response.hex())
                    read_server_response(response)
            except Exception as e:
                print(f"Socket error: {e}")

        if sys.stdin in ready:
            user_input = sys.stdin.readline().strip()
            if user_input.lower() == "q":
                print("Exiting client...")
                break
            else:
                # Send message via ChannelData instead of Send Indication
                channel_data_packet = packetBuilder.build_channelData(channel_number, user_input)
                sock.sendto(channel_data_packet, TURN_SERVER)
                print(f"Sent message via Channel {channel_number}")

        # Send refresh packet if needed
        if time.time() - last_refresh_time >= refresh_interval:
            refresh_packet = packetBuilder.build_refresh()
            sock.sendto(refresh_packet, TURN_SERVER)
            channel_bind_packet = packetBuilder.build_channelBind(peer_ip, peer_port, channel_number)
            print(f"Sending Channel Bind Request (Channel {channel_number})...")
            sock.sendto(channel_bind_packet, TURN_SERVER)
            print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
            last_refresh_time = time.time()

# ----------------------
# Quick Message Listener
# ----------------------
def start_message_listener(ip, port):
    turn_server = ip  # TURN server's IP
    turn_port = int(port)  # TURN server's port
    TURN_SERVER = (turn_server, turn_port)

    # Build Allocate Packet
    alloc_packet = packetBuilder.build_alloc()

    # Create and configure socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)  # Non-blocking socket
    sock.settimeout(None)  # No timeout

    try:
        # Send Allocate request to the TURN server
        print(f"Sending Allocate packet to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, TURN_SERVER)

        # Wait for response
        ready, _, _ = select.select([sock], [], [], 5)
        if sock in ready:
            response, addr = sock.recvfrom(4096)
            print(f"Received response from {addr}")
            if response:
                print("Response (hex):", response.hex())
                read_server_response(response)
        else:
            print("No response received from TURN server.")

    except Exception as e:
        print(f"Error: {e}")

    # Start Listening Loop
    last_refresh_time = time.time()
    refresh_interval = 60  # Refresh every 1 minute

    print("Listening for messages. Press 'q' to quit.")

    while True:
        # Calculate time until next refresh
        time_until_refresh = max(0, refresh_interval - (time.time() - last_refresh_time))

        # Wait for socket activity or user input
        ready, _, _ = select.select([sock, sys.stdin], [], [], time_until_refresh)

        if sock in ready:
            try:
                response, addr = sock.recvfrom(4096)
                print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")

                if response:
                    print("Response (hex):", response.hex())
                    read_server_response(response)
            except Exception as e:
                print(f"Socket error: {e}")

        if sys.stdin in ready:
            user_input = sys.stdin.readline().strip().lower()
            if user_input == "q":
                print("Exiting listener...")
                break

        # Send refresh packet if needed
        if time.time() - last_refresh_time >= refresh_interval:
            refresh_packet = packetBuilder.build_refresh()
            sock.sendto(refresh_packet, TURN_SERVER)
            print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
            last_refresh_time = time.time()

# -----------------
# Send File Feature
# -----------------

# -------------------
# Sending File Client
# -------------------
def start_send_file_client(ip, port):
    turn_server = ip  # TURN server's IP
    turn_port = int(port)  # Default TURN port
    peer_ip = input("IP of Peer: ")
    peer_port = int(input("Port of peer: "))
    TURN_SERVER = (turn_server, turn_port)

    # Build necessary TURN packets
    alloc_packet = packetBuilder.build_alloc()
    create_perm_packet = packetBuilder.build_createPerm(peer_ip, peer_port)
    
    # Create and configure socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(None)
    
    try:
        # Allocate relay on TURN server
        print(f"Sending allocation request to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, TURN_SERVER)
        response, addr = sock.recvfrom(4096)
        print(f"Received response from {addr}")
        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)
        
        # Create permission for peer communication
        print(f"Sending Create Permission request to {turn_server}:{turn_port}")
        sock.sendto(create_perm_packet, TURN_SERVER)
        response, addr = sock.recvfrom(4096)
        print(f"Received response from {addr}")
        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)
    except socket.timeout:
        print("No response received (timeout).")
    except Exception as e:
        print(f"Error: {e}")
    
    # Start message loop
    last_refresh_time = time.time()
    refresh_interval = 60  # Refresh interval (1 minute)

    file_path = input("Enter in the path of the file to be sent: ")
    try:
        with open(file_path, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: File not found...")
        return
    
    while True:
        time_until_refresh = max(0, refresh_interval - (time.time() - last_refresh_time))
        ready, _, _ = select.select([sock, sys.stdin], [], [], time_until_refresh)
        
        if sock in ready:
            try:
                response, addr = sock.recvfrom(4096)
                print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")
                if response:
                    print("Response (hex):", response.hex())
                    read_server_response(response)
            except Exception as e:
                print(f"Socket error: {e}")
        
        if sys.stdin in ready:
            user_input = sys.stdin.readline().strip()
            if user_input == "q":
                print("Exiting client...")
                break
            else:
                send_packet = packetBuilder.build_send_indication(peer_ip, peer_port, user_input)
                sock.sendto(send_packet, TURN_SERVER)
        
        if time.time() - last_refresh_time >= refresh_interval:
            refresh_packet = packetBuilder.build_refresh()
            sock.sendto(refresh_packet, TURN_SERVER)
            print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
            last_refresh_time = time.time()

# ------------------
# Send File Listener
# ------------------
def start_file_listener(ip, port):
    turn_server = ip  # TURN server's IP
    turn_port = int(port)  # Default TURN port
    TURN_SERVER = (turn_server, turn_port)
    
    # Build allocation packet
    alloc_packet = packetBuilder.build_alloc()
    
    # Create and configure socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.settimeout(None)
    
    try:
        # Send allocation request
        print(f"Sending allocation request to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, TURN_SERVER)
        response, addr = sock.recvfrom(4096)
        print(f"Received response from {addr}")
        if response:
            print("Response (hex):", response.hex())
            read_server_response(response)
    except socket.timeout:
        print("No response received (timeout).")
    except Exception as e:
        print(f"Error: {e}")
    
    # Start listening loop
    last_refresh_time = time.time()
    refresh_interval = 60  # Refresh interval (1 minute)
    print("Listening for incoming file data. Press 'q' to quit.")
    
    while True:
        time_until_refresh = max(0, refresh_interval - (time.time() - last_refresh_time))
        ready, _, _ = select.select([sock, sys.stdin], [], [], time_until_refresh)
        
        # TODO: Implement file receiving functionality here
        # if sock in ready:
        #     try:
        #         response, addr = sock.recvfrom(4096)
        #         print(f"Received data from {addr} at {time.strftime('%H:%M:%S')}")
        #         # Process received file chunks
        #     except Exception as e:
        #         print(f"Socket error: {e}")
        
        if sys.stdin in ready:
            user_input = sys.stdin.readline().strip().lower()
            if user_input == "q":
                print("Exiting listener...")
                break
        
        if time.time() - last_refresh_time >= refresh_interval:
            refresh_packet = packetBuilder.build_refresh()
            sock.sendto(refresh_packet, TURN_SERVER)
            print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
            last_refresh_time = time.time()
  
# --------------------
# Remote Shell Feature
# --------------------

# ------------------------------------
# Remote Shell Client
# ------------------------------------
def get_shell_client(ip, port):
    turn_server = ip  
    turn_port = int(port)  
    peer_ip = input("IP of Peer: ")
    peer_port = int(input("Port of peer: "))
    TURN_SERVER = (turn_server, turn_port)

    # Build necessary packets
    alloc_packet = packetBuilder.build_alloc()
    create_perm_packet = packetBuilder.build_createPerm(peer_ip, peer_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(None)

    try:
        # Send Allocate packet
        print(f"Sending Allocate packet to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, TURN_SERVER)

        # Receive response
        response, addr = sock.recvfrom(4096)
        print(f"Received response from {addr}")

        if response:
            print(f"Response (hex): {response.hex()}")
            read_server_response(response)

        # Send Create Permission packet
        print(f"Sending Create Permission packet to {turn_server}:{turn_port}")
        sock.sendto(create_perm_packet, TURN_SERVER)

        # Receive response
        response, addr = sock.recvfrom(4096)
        print(f"Received response from {addr}")

        if response:
            print(f"Response (hex): {response.hex()}")
            read_server_response(response)

    except socket.timeout:
        print("No response received (timeout).")
    except Exception as e:
        print(f"Error: {e}")

    # Start Channel Binding
    channel_number = random.randint(0x4000, 0x7FFF)
    print(f"CHANNEL NUMBER: {channel_number}")
    channel_bind_packet = packetBuilder.build_channelBind(peer_ip, peer_port, channel_number)
    sock.sendto(channel_bind_packet, TURN_SERVER)

    response, addr = sock.recvfrom(4096)
    print(f"Received response from {addr}")

    if response:
        print(f"Response (hex): {response.hex()}")
        read_server_response(response)

    last_refresh_time = time.time()
    refresh_interval = 60  # Refresh every minute

    print("Send quick messages. Enter 'q' to quit.")

    while True:
        time_until_refresh = max(0, refresh_interval - (time.time() - last_refresh_time))

        ready, _, _ = select.select([sock, sys.stdin], [], [], time_until_refresh)

        if sock in ready:
            try:
                response, addr = sock.recvfrom(4096)
                print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")

                if response:
                    print(f"Response (hex): {response.hex()}")
                    read_server_response(response)
            except Exception as e:
                print(f"Socket error: {e}")

        if sys.stdin in ready:
            print("> ", end="")
            command = sys.stdin.readline().strip()
            if command == "q":
                print("Exiting client...")
                break
            else:
                send_packet = packetBuilder.build_channelData(channel_number, command)
                sock.sendto(send_packet, TURN_SERVER)

        if time.time() - last_refresh_time >= refresh_interval:
            refresh_packet = packetBuilder.build_refresh()
            sock.sendto(refresh_packet, TURN_SERVER)
            print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
            last_refresh_time = time.time()

# ------------------------------------
# Remote Shell Listener
# ------------------------------------
def start_shell_listener(ip, port, channel_number):
    turn_server = ip  
    turn_port = int(port)  
    TURN_SERVER = (turn_server, turn_port)
    client_ip = input("IP of Client: ")
    client_port = int(input("Port of Client: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.settimeout(None)

    try:
        # Send Allocate packet
        alloc_packet = packetBuilder.build_alloc()
        print(f"Sending Allocate packet to {turn_server}:{turn_port}")
        sock.sendto(alloc_packet, TURN_SERVER)

        # Receive response
        response, addr = sock.recvfrom(4096)
        print(f"Received response from {addr}")

        if response:
            print(f"Response (hex): {response.hex()}")
            read_server_response(response)

    except socket.timeout:
        print("No response received (timeout).")
    except Exception as e:
        print(f"Error: {e}")

    # Bind Channel
    channel_bind_packet = packetBuilder.build_channelBind(client_ip, client_port, channel_number)
    sock.sendto(channel_bind_packet, TURN_SERVER)

    last_refresh_time = time.time()
    refresh_interval = 60  # Refresh every minute

    print("Listening for messages. Press 'q' to quit.")

    while True:
        time_until_refresh = max(0, refresh_interval - (time.time() - last_refresh_time))

        ready, _, _ = select.select([sock, sys.stdin], [], [], time_until_refresh)

        if sock in ready:
            try:
                response, addr = sock.recvfrom(4096)
                print(f"Received command from {addr} at {time.strftime('%H:%M:%S')}")

                command = response.decode("utf-8").strip()
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                output = result.stdout if result.stdout else result.stderr
                output = output.strip() if output else "EXECUTION WITH NO OUTPUT..."

                # Send output back
                send_data_packet = packetBuilder.build_channelData(channel_number, output)
                sock.sendto(send_data_packet, TURN_SERVER)
                print("Sent command output back to client.")
            except Exception as e:
                print(f"Socket error: {e}")

        if sys.stdin in ready:
            user_input = sys.stdin.readline().strip().lower()
            if user_input == "q":
                print("Exiting listener...")
                break

        if time.time() - last_refresh_time >= refresh_interval:
            refresh_packet = packetBuilder.build_refresh()
            sock.sendto(refresh_packet, TURN_SERVER)
            print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
            last_refresh_time = time.time()

# ------------------------------------
# Helper Function: Parse Server Response
# ------------------------------------
def read_server_response(response):    
    # Unpack the STUN header
    msg_type, msg_length, magic_cookie, transaction_id = struct.unpack_from("!HHI12s", response, 0)
    
    print(f"MSG_TYPE: {STUN_MESSAGE_TYPES.get(msg_type)}")
    print(f"MSG_LENGTH: {msg_length}")
    print(f"MAGIC_COOKIE: {hex(magic_cookie)}")
    print(f"TRANSACTION_ID: {transaction_id.hex()}")

    offset = 20  # Start of attributes
    MAGIC_COOKIE = 0x2112A442  # STUN Magic Cookie

    # Parse Attributes
    while offset < len(response):
        attr_type, attr_length = struct.unpack_from("!HH", response, offset)
        offset += 4  # Move past type and length

        attr_value = response[offset : offset + attr_length]
        offset += attr_length  # Move past value

        match attr_type:
            case 0x000D:  # LIFETIME
                lifetime = struct.unpack("!I", attr_value)[0]
                print(f"Lifetime\n\tValue: {lifetime} seconds")

            case 0x0020:  # XOR-MAPPED-ADDRESS
                family, xor_port = struct.unpack("!HH", attr_value[:4])
                xor_ip = struct.unpack("!I", attr_value[4:])[0] ^ MAGIC_COOKIE
                ip_addr = ".".join(map(str, xor_ip.to_bytes(4, 'big')))
                port = xor_port ^ 0x2112
                print(f"XOR-MAPPED-ADDRESS\n\tIP: {ip_addr}\n\tPORT: {port}")

            case 0x0008:  # RESERVED ADDRESS (another XOR-MAPPED-ADDRESS)
                family, xor_port = struct.unpack("!HH", attr_value[:4])
                xor_ip = struct.unpack("!I", attr_value[4:])[0] ^ MAGIC_COOKIE
                ip_addr = ".".join(map(str, xor_ip.to_bytes(4, 'big')))
                port = xor_port ^ 0x2112
                print(f"Reserved XOR-MAPPED-ADDRESS\n\tIP: {ip_addr}\n\tPORT: {port}")

            case 0x8022:  # SOFTWARE
                software_version = attr_value.decode(errors="ignore")
                print(f"Software\n\tValue: {software_version}")

            case 0x8028:  # FINGERPRINT
                fingerprint = struct.unpack("!I", attr_value)[0]
                print(f"Fingerprint\n\tValue: {fingerprint}")

            case 0x0013:  # DATA
                data = attr_value
                print(f"🔹 DATA (Received from peer):\n\t{data.hex()}") 
                print(f"\tDecoded: {data.decode()}")

            case 0x0012:  # XOR-PEER-ADDRESS (PEER)
                reserved, family, xor_port = struct.unpack("!BBH", attr_value[:4])  # Proper unpacking
                if family == 0x01:  # IPv4
                    xor_ip_bytes = attr_value[4:8]  # Extract XOR'ed IP
                    xor_ip = bytes([
                        xor_ip_bytes[i] ^ ((MAGIC_COOKIE >> (8 * (3 - i))) & 0xFF) 
                        for i in range(4)
                    ])  
                    peer_ip = ".".join(map(str, xor_ip))  # Convert to IPv4 string

                peer_port = xor_port ^ 0x2112  # XOR the port with the top 16 bits of the magic cookie
                print(f"🔹 XOR-PEER-ADDRESS\n\tIP: {peer_ip}\n\tPORT: {peer_port}")
            case 0x0001:  # Mapped Address Attribute
                family, xor_port = struct.unpack_from("!BH", response, offset)
                xor_port ^= (magic_cookie >> 16)  # Decode port
                
                if family == 0x01:  # IPv4
                    xor_ip = struct.unpack_from("!I", response, offset)[0]
                    xor_ip ^= magic_cookie  # Decode IPv4 address
                    mapped_ip = socket.inet_ntoa(struct.pack("!I", xor_ip))

                print(f"    MAPPED ADDRESS ATTRIBUTE\n\tIP: {mapped_ip}\n\tPORT: {xor_port}")
            case 0x007:  # DATA INDICATION
                print("Received Data Indication")
            case 0x0016:
                print("Relayed Transport Address (RTA)")
                reserved, family, xor_port = struct.unpack("!BBH", attr_value[:4])

                if family == 0x01:  # IPv4
                    xor_ip_bytes = attr_value[4:8]  # Extract XOR'ed IP
                    xor_ip = bytes([
                        xor_ip_bytes[i] ^ ((MAGIC_COOKIE >> (8 * (3 - i))) & 0xFF) 
                        for i in range(4)
                    ])  
                    relayed_ip = ".".join(map(str, xor_ip))  # Convert to IPv4 string

                relayed_port = xor_port ^ 0x2112  # Decode port
                print(f"🔹 XOR-RELAYED-ADDRESS (RTA)\n\tIP: {relayed_ip}\n\tPORT: {relayed_port}")
            case _:
                print(f"Unknown Type: {hex(attr_type)}")