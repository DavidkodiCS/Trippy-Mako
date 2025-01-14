import struct
import os

class TURN:
    def __init__(self, clientTransportIP, clientPort, serverTransportIP, serverPort, transportProtocol):
        self.clientTransportIP = clientTransportIP
        self.clientPort = clientPort
        self.serverTransportIP = serverTransportIP
        self.serverPort = serverPort
        self.transportProtocol = transportProtocol
        self.turnTuple = (self.clientTransportIP, self.clientPort, self.serverTransportIP, self.serverPort, self.transportProtocol)

    ## Message Builders
    def build_alloc():
        STUN_HEADER_FORMAT = "!HHI12s"
        MESSAGE_TYPE = 0x003
        MAGIC_COOKIE = 0x2112A442
        TRANSACTION_ID = os.urandom(12)

        #Allocate Requires REQUESTED-TRANSPORT
        REQUESTED_TRANSPORT_TYPE = 0x0019
        REQUESTED_TRANSPORT_LENGTH = 4
        UDP_TRANSPORT = 0x06
        RESERVED = 0x00

        requested_transport = struct.pack(
            "!HHBB2x",
            REQUESTED_TRANSPORT_TYPE,
            REQUESTED_TRANSPORT_LENGTH,
            UDP_TRANSPORT,
            RESERVED
        )

        rtLen = len(requested_transport)

        header = struct.pack(
            STUN_HEADER_FORMAT,
            MESSAGE_TYPE,
            rtLen,
            MAGIC_COOKIE,
            TRANSACTION_ID
        )

        alloc_packet = header + requested_transport
        return alloc_packet

    def build_refresh():
        STUN_HEADER_FORMAT = "!HHI12s"
        MESSAGE_TYPE = 0x004
        MAGIC_COOKIE = 0x2112A442
        TRANSACTION_ID = os.urandom(12)

    def build_send():
        STUN_HEADER_FORMAT = "!HHI12s"
        MESSAGE_TYPE = 0x006
        MAGIC_COOKIE = 0x2112A442
        TRANSACTION_ID = os.urandom(12)

    def build_data():
        STUN_HEADER_FORMAT = "!HHI12s"
        MESSAGE_TYPE = 0x007
        MAGIC_COOKIE = 0x2112A442
        TRANSACTION_ID = os.urandom(12)

    def build_createPerm():
        STUN_HEADER_FORMAT = "!HHI12s"
        MESSAGE_TYPE = 0x008
        MAGIC_COOKIE = 0x2112A442
        TRANSACTION_ID = os.urandom(12)

    def build_channelBind():
        STUN_HEADER_FORMAT = "!HHI12s"
        MESSAGE_TYPE = 0x009
        MAGIC_COOKIE = 0x2112A442
        TRANSACTION_ID = os.urandom(12)


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
    
