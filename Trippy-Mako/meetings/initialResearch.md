# Meeting Notes

## Week 1: Individual Write-Ups on TURN Knowledge, Libraries, and Implementation

### Team Contributions

#### David

- **Documentation**: Use Sphinx to document code.
- **TURN Protocol**: Focus on TURN in Client-Server models.
- **Resources**:
  - [GitHub Turn Proxy](https://github.com/trichimtrich/turnproxy)
  - TURN RFC, STUN RFC, TURN RFC - Server Auto Discovery.
- **Key Meetings**: VTC with Capt Burn and Meris.
- **Discussion Topics**:
  - Utility of TURN in the field and its relevance.
  - Comparison of TURN vs. Wireguard (consult with Capt Burn).
  - Linux vs. Windows networking stack considerations.
- **Project Management**:
  - Scrum board for task tracking.
  - Use Gantt charts for managing timelines.
  - Importance of specifying dates.
- **Proposal**: Emphasis on explaining the TURN protocol in detail.
- **Initial Sprint Idea**:
  - Set up two VMs (vm1 and vm3) behind “two symmetric NATs.”
  - Create a third VM (vm2) to act as the TURN server using `python3 -m http.server 8000` for basic HTTP requests.
  - Explore options for a TURN-like server with more advanced functionality.

#### Notes from VirtualBox Setup

- **VMs & Network Setup**:
  - 5 VMs in total with 3 virtual networks (Host-Only Networks).
  - Use VirtualBox NAT networks for controlled VM communication and access to the internet.
  - Routers need two NICs: one for "Internet" and one for their private networks.
  - Clients and the TURN server will have one NIC on their respective networks.

- **Network Overview**:
  - **Networks**:
    1. Internet
    2. Client A Network
    3. Client B Network
  - **VMs**:
    - 1 TURN Server VM: Attached to the Internet network.
    - 2 Routers (VyOS or pfSense): One NIC for the Internet, one for the respective client network.
    - 2 Clients: Each attached to their respective networks.

- **Important Considerations**:
  - Implementing TURN is the most challenging aspect of the project.
  - Be prepared to explain the TURN protocol clearly to a professor.
  - Python libraries will handle TURN functions, with the main program acting as the tool that utilizes these functions.

---

#### Meris

- **TURN Overview**:
  - TURN (Traversal Using Relays around NAT) servers facilitate connections between hosts when STUN fails.
  - Typically used in WebRTC (Web Real-Time Connection) to establish peer-to-peer connections.
  - STUN servers identify IPs, and if unsuccessful, TURN servers relay the information.
- **Project Focus**: Use TURN to abstract the source of data transfer.
- **Implementation Notes**:
  - Using TURN may increase latency due to relaying but adds security by hiding the data source.
  - **Suggested Libraries**: Consider using `aiortc` for Python for WebRTC integration.
  - **Example Code**: Provided a basic Python script using `aiortc` for TURN server setup.
- **Authentication**:
  - TURN servers require username/password authentication.
  - Consider using the Python `requests` library for handling credentials.
  - Research salting/hashing techniques for secure password management.
- **Communication**:
  - Use WebSockets for signaling between hosts.

---

#### Charlie

- **TURN Overview**:
  - TURN facilitates communication when direct paths between hosts fail due to NAT configurations.
  - Acts as a relay when hole-punching techniques do not work.
  - Designed to be used with SIP protocol for multimedia sessions.
- **NAT Challenges**:
  - Hosts behind “not well-behaved” NATs (e.g., address-dependent mapping) require TURN for communication.
- **Key Components**:
  - TURN client, TURN server, and peers.
  - TURN client obtains a **relayed transport address** (RTA) for communication through the TURN server.
  - Server relays packets between the client and its peers.
- **STUN vs. TURN**:
  - STUN identifies public IPs and ports but is not a complete NAT traversal solution like TURN.
  - TURN is often used with ICE (Interactive Connectivity Establishment) but can be implemented without it.

---

## RFC 5766 Notes: TURN Protocol

- TURN allows clients to create an allocation on the server.
- Clients send data to the TURN server, which then relays the data to the peer as a UDP datagram.
- Key operations include sending and receiving `Allocate` requests, `Refresh` requests, `CreatePermission` requests, `Send Indications`, `ChannelBind` requests, and handling `ChannelData` messages.
- **Relayed Transport Address (RTA)**:
  - The client needs to share the RTA with peers.
  - TURN can be used alongside ICE for multimedia applications, offering a fallback when direct connections fail.

---

## Draft of Tasks for TURN Implementation

- Sending an Allocate Request
- Receiving an Allocate Request
- Receiving an Allocate Success Response
- Receiving an Allocate Error Response
- Sending a Refresh Request
- Receiving a Refresh Request
- Receiving a Refresh Response
- Forming a CreatePermission Request
- Receiving a CreatePermission Request
- Receiving a CreatePermission Response
- Forming a Send Indication
- Receiving a Send Indication
- Receiving a UDP Datagram
- Receiving a Data Indication
- Sending a ChannelBind Request
- Receiving a ChannelBind Response
- Formatting a ChannelData Message
- Sending a ChannelData Message
- Receiving a ChannelData Message
- Relaying Data from the Peer
