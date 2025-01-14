import struct
import socket
import os

class TURN:
    def __init__(self, clientTransportIP, clientPort, serverTransportIP, serverPort, transportProtocol):
        self.clientTransportIP = clientTransportIP
        self.clientPort = clientPort
        self.serverTransportIP = serverTransportIP
        self.serverPort = serverPort
        self.transportProtocol = transportProtocol
        self.turnTuple = (self.clientTransportIP, self.clientPort, self.serverTransportIP, self.serverPort, self.transportProtocol)

    ## Description of function
    def sendAllocation(self):
        STUN_MAGIC_COOKIE = 0x2112A442
        STUN_ALLOCATE_REQUEST = 0x0003

        # Generate a unique transaction ID (12 bytes)
        transaction_id = os.urandom(12)

        # Message length initially 0 (no attributes yet)
        message_length = 0

        LIFETIME_ATTR_TYPE = 0x000D
        lifetime_value = 3600  # Lifetime in seconds

        # Pack the header (Type, Length, Magic Cookie, Transaction ID)
        header = struct.pack(
            "!HHI12s",  # Network byte order: 2 bytes, 2 bytes, 4 bytes, 12 bytes
            STUN_ALLOCATE_REQUEST,  # Message type
            message_length,         # Message length
            STUN_MAGIC_COOKIE,      # Magic cookie
            transaction_id          # Transaction ID
        )



        #send 5 tuple to TURN server
        return 0
    
    ##Description of function
    def sendRefresh(self):
        return 0
    
