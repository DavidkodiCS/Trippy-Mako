import socket
import struct
import sys
import time
import packetBuilder
import security
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

PEER_PUBLIC_KEY = ""


class TurnTM:
    def __init__(self, turnInfo):
        ip, port, encrypted, verbose = turnInfo
        
        self.turn_server_ip = ip
        self.turn_server_port = port
        
        if encrypted == "0": self.encrypted = False 
        else: self.encrypted = True
        
        self.verbose = verbose

    # ----------------------#
    # Quick Message Feature #
    # ----------------------#

    # ---------------------#
    # Quick Message Client #
    # ---------------------#
    
    def start_quick_message_client(self):
        TURN_SERVER = (self.turn_server_ip, int(self.turn_server_port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(None)  # No timeout
        sock.setblocking(False)  # Non-blocking socket

        # Generate a random valid channel number (RFC 5766: between 0x4000 - 0x7FFF)
        # HARDCODED VALUE
        channel_number = 0x4001

        # Establish initial TURN connection
        RTA_TUP = self._create_turn_connection(sock, TURN_SERVER, channel_number, self.verbose)
        if RTA_TUP == -1:
            return
        
        # ## Perform Key Exchange
        # if PEER_PUBLIC_KEY == "":
        #     PEER_PUBLIC_KEY = _key_exchange(sock, TURN_SERVER, channel_number)

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
                    if self.verbose :
                        print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")

                    if response:
                            print("Response (hex):", response.hex())
                            self._read_server_response(response, self.verbose)
                            self._parse_channel_response(response, self.encrypted, self.verbose)
                except Exception as e:
                    print(f"Socket error: {e}")

            if sys.stdin in ready:
                user_input = sys.stdin.readline().strip()
                if user_input.lower() == "q":
                    print("Exiting client...")
                    break
                else:
                    #Send message via ChannelData instead of Send Indication
                    if self.encrypted:
                        security.encrypt_message(user_input)
                    channel_data_packet = packetBuilder.build_channelData(channel_number, user_input)
                    sock.sendto(channel_data_packet, TURN_SERVER)
                    if self.verbose :
                        print(f"Sent message via Channel {channel_number}")

            # Send refresh packet if needed
            if time.time() - last_refresh_time >= refresh_interval:
                refresh_packet = packetBuilder.build_refresh()
                sock.sendto(refresh_packet, TURN_SERVER)
                channel_bind_packet = packetBuilder.build_channelBind(RTA_TUP[0], RTA_TUP[1], channel_number)
                if self.verbose :
                    print(f"Sending Channel Bind Request (Channel {channel_number})...")
                sock.sendto(channel_bind_packet, TURN_SERVER)
                if self.verbose :
                    print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
                last_refresh_time = time.time()

    # -----------------------#
    # Quick Message Listener #
    # -----------------------#
    def start_message_listener(self):
        TURN_SERVER = (self.turn_server_ip, int(self.turn_server_port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(None)  # No timeout
        sock.setblocking(False)  # Non-blocking socket
        # Generate a random valid channel number (RFC 5766: between 0x4000 - 0x7FFF)
        # HARDCODED VALUE
        channel_number = 0x4001

        # Establish initial TURN connection
        RTA_TUP = self._create_turn_connection(sock, TURN_SERVER, channel_number, self.verbose)
        if RTA_TUP == -1:
            return

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
                    if self.verbose :
                        print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")

                    if response:
                        if self.verbose :
                            print("Response (hex):", response.hex())
                            
                        self._read_server_response(response, self.verbose)
                        self._parse_channel_response(response, self.verbose)
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
                channel_bind_packet = packetBuilder.build_channelBind(RTA_TUP[0], RTA_TUP[1], channel_number)
                if self.verbose :
                    print(f"Sending Channel Bind Request (Channel {channel_number})...")
                sock.sendto(channel_bind_packet, TURN_SERVER)
                if self.verbose :
                    print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
                last_refresh_time = time.time()


    # -----------------
    # Send File Feature
    # -----------------

    # -------------------
    # Sending File Client
    # -------------------
    def start_send_file_client(self):
        TURN_SERVER = (self.turn_server_ip, int(self.turn_server_port))
        # Create and configure socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(None)
        sock.setblocking(False)
        # Generate a random valid channel number (RFC 8656: between 0x4000 - 0x7FFF)
        # HARDCODED VALUE
        channel_number = 0x4001

        # Establish initial TURN connection
        RTA_TUP = self._create_turn_connection(sock, TURN_SERVER, channel_number, self.verbose)
        if RTA_TUP == -1:
            return

        file_path = input("Enter in the path of the file to be sent: ")
        
        refresh_packet = packetBuilder.build_refresh()
        sock.sendto(refresh_packet, TURN_SERVER)
        if self.verbose :
            print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
        
        try:
            with open(file_path, "r") as f:
                print("File read...")
            
                while True:        
                    data = f.read(1024)
                    if not data:
                        break
                    channel_data_packet = packetBuilder.build_channelData(channel_number, data)
                    sock.sendto(channel_data_packet, TURN_SERVER)

                print("File successfully sent!")
        except Exception as e:
            print(f"Error sending file: {e}")
        except FileNotFoundError:
            print("Error: File not found...")
            return

    # ------------------
    # Send File Listener
    # ------------------
    def start_file_listener(self):
        TURN_SERVER = (self.turn_server_ip, int(self.turn_server_port))
        # Create and configure socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(False)
        sock.settimeout(None)    
        # Generate a random valid channel number (RFC 5766: between 0x4000 - 0x7FFF)
        # HARDCODED VALUE
        channel_number = 0x4001
        
        ## Filename
        filename = input("Please choose a filename or file to be written to: ")

        # Establish initial TURN connection
        RTA_TUP = self._create_turn_connection(sock, TURN_SERVER, channel_number, self.verbose)
        if RTA_TUP == -1:
            return   
        
        refresh_packet = packetBuilder.build_refresh()
        sock.sendto(refresh_packet, TURN_SERVER)
        if self.verbose :
            print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
        
        print("Listening for incoming file data.")
        
        try:
            with open(filename, 'wb') as f:
                sock.settimeout(10) 
                while True:
                    data = sock.recv(1024)
                    ##file_data = _parse_channel_response(data, verbose)
                    if not data:
                        f.close()
                        break
                    f.write(data)

                print(f"Received and saved file as {filename}")
        except Exception as e:
            print(f"Received and saved file as {filename}")
    
    # --------------------
    # Remote Shell Feature
    # --------------------

    # ------------------------------------
    # Remote Shell Client
    # ------------------------------------
    def start_shell_client(self):
        TURN_SERVER = (self.turn_server_ip, int(self.turn_server_port))    
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(None)
        sock.setblocking(False)
        # Generate a random valid channel number (RFC 5766: between 0x4000 - 0x7FFF)
        # HARDCODED VALUE
        channel_number = 0x4001

        # Establish initial TURN connection
        RTA_TUP = self._create_turn_connection(sock, TURN_SERVER, channel_number, self.verbose)
        if RTA_TUP == -1:
            return

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
                        if self.verbose :
                            print(f"Response (hex): {response.hex()}")
                            
                        self._read_server_response(response, self.verbose)    
                        self._parse_channel_response(response, self.verbose, self.encrypted, "NULL")
                except Exception as e:
                    print(f"Socket error: {e}")

            if sys.stdin in ready:
                print("> ", end="")
                command = sys.stdin.readline().strip()
                if command == "q":
                    print("Exiting client...")
                    break
                else:
                    send_packet = packetBuilder.build_channelData(channel_number, command.strip())
                    sock.sendto(send_packet, TURN_SERVER)

            # Send refresh packet if needed
            if time.time() - last_refresh_time >= refresh_interval:
                refresh_packet = packetBuilder.build_refresh()
                sock.sendto(refresh_packet, TURN_SERVER)
                channel_bind_packet = packetBuilder.build_channelBind(RTA_TUP[0], RTA_TUP[1], channel_number)
                if self.verbose :
                    print(f"Sending Channel Bind Request (Channel {channel_number})...")
                sock.sendto(channel_bind_packet, TURN_SERVER)
                if self.verbose :
                    print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
                last_refresh_time = time.time()

    # ------------------------------------
    # Remote Shell Listener
    # ------------------------------------
    def start_shell_listener(self):
        TURN_SERVER = (self.turn_server_ip, int(self.turn_server_port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        sock.settimeout(None)
        sock.setblocking(False)
        
        # Generate a random valid channel number (RFC 5766: between 0x4000 - 0x7FFF)
        # HARDCODED VALUE
        channel_number = 0x4001

        # Establish initial TURN connection
        RTA_TUP = self._create_turn_connection(sock, TURN_SERVER, channel_number, self.verbose)
        if RTA_TUP == -1:
            return   

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

                    command = self._parse_channel_response(response, self.verbose, self.encrypted, "NULL")
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    output = result.stdout if result.stdout else result.stderr
                    output = output.strip() if output else "EXECUTION WITH NO OUTPUT..."

                    # Send output back
                    send_data_packet = packetBuilder.build_channelData(channel_number, output)
                    sock.sendto(send_data_packet, TURN_SERVER)
                    
                    if self.verbose :
                        print("Sent command output back to client.")
                except Exception as e:
                    pass

            if sys.stdin in ready:
                user_input = sys.stdin.readline().strip().lower()
                if user_input == "q":
                    print("Exiting listener...")
                    break

            # Send refresh packet if needed
            if time.time() - last_refresh_time >= refresh_interval:
                refresh_packet = packetBuilder.build_refresh()
                sock.sendto(refresh_packet, TURN_SERVER)
                channel_bind_packet = packetBuilder.build_channelBind(RTA_TUP[0], RTA_TUP[1], channel_number)
                if self.verbose :
                    print(f"Sending Channel Bind Request (Channel {channel_number})...")
                sock.sendto(channel_bind_packet, TURN_SERVER)
                if self.verbose :
                    print(f"Sent Refresh packet at {time.strftime('%H:%M:%S')}")
                last_refresh_time = time.time()

    # ------------------------------------
    # Helper Function: Parse Server Response
    # ------------------------------------
    def _read_server_response(self, response, verbose):    
        # Unpack the STUN header
        try:
            msg_type, msg_length, magic_cookie, transaction_id = struct.unpack_from("!HHI12s", response, 0)
        except: 
            print("Channel Data Message...")
            return
            
        offset = 20  # Start of attributes

        if verbose:
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
                    if verbose:
                        print(f"Lifetime\n\tValue: {lifetime} seconds")

                case 0x0020:  # XOR-MAPPED-ADDRESS
                    family, xor_port = struct.unpack("!HH", attr_value[:4])
                    xor_ip = struct.unpack("!I", attr_value[4:])[0] ^ MAGIC_COOKIE
                    ip_addr = ".".join(map(str, xor_ip.to_bytes(4, 'big')))
                    port = xor_port ^ 0x2112
                    if verbose:
                        print(f"XOR-MAPPED-ADDRESS\n\tIP: {ip_addr}\n\tPORT: {port}")

                case 0x0008:  # RESERVED ADDRESS (another XOR-MAPPED-ADDRESS)
                    family, xor_port = struct.unpack("!HH", attr_value[:4])
                    xor_ip = struct.unpack("!I", attr_value[4:])[0] ^ MAGIC_COOKIE
                    ip_addr = ".".join(map(str, xor_ip.to_bytes(4, 'big')))
                    port = xor_port ^ 0x2112
                    if verbose:
                        print(f"Reserved XOR-MAPPED-ADDRESS\n\tIP: {ip_addr}\n\tPORT: {port}")

                case 0x8022:  # SOFTWARE
                    software_version = attr_value.decode(errors="ignore")
                    if verbose:
                        print(f"Software\n\tValue: {software_version}")

                case 0x8028:  # FINGERPRINT
                    fingerprint = struct.unpack("!I", attr_value)[0]
                    if verbose:
                        print(f"Fingerprint\n\tValue: {fingerprint}")

                case 0x0013:  # DATA
                    data = attr_value
                    if verbose:
                        print(f"🔹 DATA (Received from peer):\n\t{data.hex()}") 
                        print(f"\tDecoded: {data.decode(errors="ignore")}")

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
                    if verbose:
                        print(f"🔹 XOR-PEER-ADDRESS\n\tIP: {peer_ip}\n\tPORT: {peer_port}")
                
                case 0x0001:  # Mapped Address Attribute
                    family, xor_port = struct.unpack_from("!BH", response, offset)
                    xor_port ^= (magic_cookie >> 16)  # Decode port
                    
                    if family == 0x01:  # IPv4
                        xor_ip = struct.unpack_from("!I", response, offset)[0]
                        xor_ip ^= magic_cookie  # Decode IPv4 address
                        mapped_ip = socket.inet_ntoa(struct.pack("!I", xor_ip))

                    if verbose:
                        print(f"    MAPPED ADDRESS ATTRIBUTE\n\tIP: {mapped_ip}\n\tPORT: {xor_port}")
                
                case 0x007:  # DATA INDICATION
                    if verbose:
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
                    ##print(f"🔹 XOR-RELAYED-ADDRESS (RTA)\n\tIP: {relayed_ip}\n\tPORT: {relayed_port}")
                    print(f"SEND THIS TO PEER: {relayed_port}")
                
                case _:
                    print(f"Unknown Type: {hex(attr_type)}")

    # ------------------------------------
    # Helper Function: Establish Connection to Turn Server
    # ------------------------------------
    def _create_turn_connection(self, sock, TURN_SERVER, channel_number, verbose):
        # Allocate Request
        alloc_packet = packetBuilder.build_alloc()
        if verbose :
            print(f"Sending Allocate packet to {TURN_SERVER[0]}:{TURN_SERVER[1]}")
        sock.sendto(alloc_packet, TURN_SERVER)

        # Wait for a response
        ready, _, _ = select.select([sock], [], [], 5)
        
        if sock in ready:
            try:
                response, addr = sock.recvfrom(4096)
                if verbose :
                    print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")

                if response:
                    print("Response (hex):", response.hex())
                    self._read_server_response(response, verbose)

            except Exception as e:
                print(f"Socket error: {e}")

        # Get Peer Information
        print("Please enter the following information before allocation timeout (1 minute)...")
        peer_ip = TURN_SERVER[0]
        peer_port = int(input("TURN PORT (RTA):"))

        # Create Permission Request
        create_perm_packet = packetBuilder.build_createPerm(peer_ip, peer_port)
        if verbose :
            print(f"Sending Create Permission packet to {TURN_SERVER[0]}:{TURN_SERVER[1]}")
        sock.sendto(create_perm_packet, TURN_SERVER)

        # Wait for a response
        ready, _, _ = select.select([sock], [], [], 5)
        
        if sock in ready:
            try:
                response, addr = sock.recvfrom(4096)
                if verbose :
                    print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")

                if response:
                    print("Response (hex):", response.hex())
                    self._read_server_response(response, verbose)

            except Exception as e:
                print(f"Socket error: {e}")

        #Send Channel Bind Request
        channel_bind_packet = packetBuilder.build_channelBind(peer_ip, peer_port, channel_number)
        if verbose :
            print(f"Sending Channel Bind Request (Channel {channel_number})...")
        sock.sendto(channel_bind_packet, TURN_SERVER)

        # Wait for a response
        ready, _, _ = select.select([sock], [], [], 5)
        
        if sock in ready:
            try:
                response, addr = sock.recvfrom(4096)
                if verbose :
                    print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")

                if response:
                    print("Response (hex):", response.hex())
                    self._read_server_response(response, verbose)

            except Exception as e:
                print(f"Socket error: {e}")

        # Refresh Allocation
        refresh_packet = packetBuilder.build_refresh()
        if verbose:
            print(f"Sending Refresh packet to {TURN_SERVER[0]}:{TURN_SERVER[1]}")
        sock.sendto(refresh_packet, TURN_SERVER)

        ready, _, _ = select.select([sock], [], [], 5)
        
        if sock in ready:
            try:
                response, addr = sock.recvfrom(4096)
                if verbose:
                    print(f"Received response from {addr} at {time.strftime('%H:%M:%S')}")

                if response:
                    print("Response (hex):", response.hex())
                    self._read_server_response(response, verbose)

            except Exception as e:
                print(f"Socket error: {e}")

        return (peer_ip, peer_port)

    # ------------------------------------
    # Helper Function: Parse Command Response
    # ------------------------------------
    def _parse_channel_response(self, response,verbose, encrypted):
        try:
            channel_number, length = struct.unpack_from("!HH", response, 0)
        except:
            return None
        message = response[4:4+length]  # Slice the message portion
        if encrypted:
            security.decrypt_message(message)
        if verbose:
            print("CHANNEL DATA MESSAGE\n")
            print(f"CHANNEL NUMBER: {channel_number}")
            print(f"LENGTH: {length}")
            print(f"MESSAGE: {message.decode(errors='ignore')}")
            print(message.decode(errors='ignore'))
            return message.decode(errors='ignore')
        else:
            print(message.decode(errors='ignore'))
            return message.decode(errors='ignore')

    ## When imported using from turnTM import * only imports these functions:
    __all__ = ["start_send_file_client", 
            "start_file_listener", 
            "start_shell_client", 
            "start_shell_listener", 
            "start_quick_message_client",
                "start_message_listener"
            ]