# TURN Research: Kreidler

## 3.1 Transports

- TURN, in this RFC, uses UDP between the server and peer. **TLS, however can be used from the client to the server**.
  - Can use TLS-over-TCP or DTLS-over-UDP.

- TURN supports TCP transport because some firewalls block UDP.
  - Maybe we can **have two functions**, TLS-over-TCP or DTLS-over-UDP. Depending on the firewall the user might encounter.
- **Section 6.2.3 of RFC 8489 has information about using cipher suites, server sertificate validation, and authentiation of TURN servers.**
- 