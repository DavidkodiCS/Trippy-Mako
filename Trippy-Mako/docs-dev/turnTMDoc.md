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

