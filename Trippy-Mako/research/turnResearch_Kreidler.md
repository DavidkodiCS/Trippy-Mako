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
  - 
- Delete allocations by sending a refresh with a lifetime of 0.
