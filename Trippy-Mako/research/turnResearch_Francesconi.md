# TURN Research: Francesconi

## RFC 8656 3.4-3.6

### 3.4 Send Mechanism

There are two mechainisms for clent and peers to exchange application data. One of the methods is the send method.

The first method is indications. Indications are specifically for communication from the client to the server. Communication from the server to the peer are done via UDP datagrams.

Send inidcations are used to send application data from client to server. A send indication contains an XOR-PEER-ADDRESS attribute which specifies the  (server-reflexive) transport address of the peer. The send indication also contains a DATA attribute containing the the application data from the client. The server takes the data in the DATA attribute and sends it in a UDP datagram to the peer using the relayed transport address as the source address.

Data indications are used in the reverse direction by transferring UDP datagrams via the TURN server. Here the server XOR-PEER-ADDRESS attribute contains the server reflexive transport address of the peer and the data is in the DATA attribute.

Data indications typically only relay UDP datagrams but some ICMP packets that are recievied at the relayed transport address are relayed as Data Indications. In this case there is an ICMP attribute contining the ICMP type and code. 

Send and Data indications cannot be authenticated allowing an attacker to send bogus Send indications to the server, relaying them to peers. This is not seen as a big issue as the client-to-server path is only half of the total path to the peer.

### 3.5 Channels

Channels are an alternative to the send mechanism. Channels have less overhead than the send mechanism.

Channels use an altetrnative packet format known as the "ChannelData message" which has a 4-byte header knows as a channel number that is bound to a specific peer and servs as a shorthand for a peer's host transport address.

To bind chanels to peers a client seds a ChannelBind request to the sever with an unbound chnell number and the transport address of the peer. Channel bindings last for 10 minutes unles refrenshed, longer than the permission lifetime. Once bound a client can use ChannelData messages to tsend the server data. The server can also relay data the opposite direction using a ChannelDatamessage.


Once a channel is bound the client can send either ChannelData messages or Send indications. Once a channel is bound the server however will always use ChannelData messages.

### 3.6 Unprivalaged TURN Servers



