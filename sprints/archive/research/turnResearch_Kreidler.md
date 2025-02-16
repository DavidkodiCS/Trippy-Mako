# TURN Research: Kreidler

## 3.1 Transports

- TURN, in this RFC, uses UDP between the server and peer. **TLS, however can be used from the client to the server**.
  - Can use TLS-over-TCP or DTLS-over-UDP.
  - Only issue with DTLS is there is a higher overhead. (doubly encrypted)

- TURN supports TCP transport because some firewalls block UDP.
  - Maybe we can **have two functions**, TLS-over-TCP or DTLS-over-UDP. Depending on the firewall the user might encounter.
- **Section 6.2.3 of RFC 8489 has information about using cipher suites, server sertificate validation, and authentiation of TURN servers.**

## 3.2 Allocations

- **Allocate Transaction**: Client sends an Allocate request to the server, and the server replies with an Allocate success response containing the **allocated relayed transport address**.
- Client must then keep the request alive so it must periodically send a **Refresh Request** to the server.
  - Refresh function is used instead of Allocate again to let the client know if the allocation *vanishes*.
- Default lifetime of an Allocation is 10 minutes.
- Delete allocations by sending a refresh with a lifetime of 0.
- **5-tuple**: (client IP address and port, server IP address and port, and transport protocol (currently one of UDP, TCP, DTLS/UDP, or TLS/TCP))
  - To create a second allocation the client must use a new host address or port.
- When the client makes a successful allocate request the TURN server will respond with it's IP and port (TURN Server Transport Address).
- Server requires that all requests be authenticated using **STUN's long-term credential mechanism**.

## 3.3 Permissions

- TURN permissions mimic the address-restricted filtering mechanism of NATs that comply with [RFC4787](https://datatracker.ietf.org/doc/html/rfc4787)
- Permissions: 0 or more. Each one is associated with an IP and lifetime.
- Client can install or refresh a permission using either a CreatePermission request or a ChannelBind request.
- Within the context of an allocation. Adding/Expiring in one allocation doesn't affect others.
- **I don't think we really have to worry about Permissions too much right away.**
- *The TURN server will only forward traffic to its client from peers that match an existing permission.* (might be important)

## 5 General Behavior

- TURN is an extension to STUN

## 6 Allocations

## 7 Creating an Allocation

## 7.1 Sending an Allocate Request

Assume this is a function
Parameters: Client transport address, Client port, server transport address, server port, transport protocol?

1. Choose host transport address (Client): Allow OS to choose unused port.
2. Choose a transport protocol: RECOMMENDED to pick UDP since that is what most TURN servers use but see 3.1 to use other protocols. We will want our information to be encrypted across the line so we will need to work around any issues here. Our implementation of authentication must comply with TURN/STUN but still be effective.
3. Client picks a server transport address (TURN server public IP) For now we can just assume the user will know the address and input it in using our CLI tool.
4. Include REQUESTED-TRANSPORT attribute (for now always assume UDP. This is not the transport protocol specified in the 5-tuple)
5. Let's just go with IPv4 for now.
6. Client can ask server to change the initial lifetime of an allocation but the server will ignore it if it is less than the default (5 mins?)

- Various attributes: REQUESTED-ADDRESS-FAMILY attribute, RESERVATION-TOKEN attribute, DONT-FRAGMENT, EVEN-PORT.
