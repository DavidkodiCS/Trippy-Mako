## TURN Research: Larkins

# 3.7: Avoid IP Fragmentation

To avoid issues with communication via the TURN protocol, packets should not be fragmented. TCP automatically handles this issue, but since we're using UDP, we'll need to implement something to combat this manually. Either messages have to have a maximum size that will allow them to be sent in whole without fragmentation or the network must have enough bandwidth to support the message size (or both). To avoid sending too much data at a time, MTUs (Maximum Transmission Units) of around 1280 octets for IPv6 and around 576 octets for IPv4 are recommended, but there are also session-specific details that must be taken into consideration (i.e. an attribute preventing fragmentation, limited bandwidth due to tunneling, differences in protocols, etc.). Message sizes of 500 bytes should not be fragmented, and ChannelData messages have the smallest overhead. Besides manually controlling the MTU size, the developer can also implement an MTU Discovery Algorithm to find the right MTU size that will avoid packet fragmentation (these algorithms are defined in RFC4821 and MTU-DATAGRAM). When using the DONT-FRAGMENT attribute, and Allocate request should also be sent by the client to make sure the server-to-peer connection supports the attribute.

# 3.8: RTP Support

TURN supports older versions of RTP (Real-time Transport Protocol) since one of its intended uses was sending voice or video between clients. As the protocol requires it, TURN will reserve both the necessary even-numbered port for communication and the next-highest port.

# 3.9: Happy Eyeballs for TURN

If a TURN server is using both IPv4 and IPv6 addresses for communication and, for example, the IPv4 path is working but the IPv6 path is not, there could be a connection delay. To bridge this gap, the server needs to query both types of DNS records for resolution (A and AAAA). For TLS-over-TCP, the Happy Eyeballs Procedure from RFC8305 is used to fix this problem (this is one possibly-applicable solution for our project). For DTLS-over-UDP, a handshake is initiated for both the IPv4 and IPv6 addresses, and the first fully-established connection is used while the other is discarded (this is the other possibly-applicable bit of information).
