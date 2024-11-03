# Capstone Proposal

## Overview

- **What are you planning to build?**
  
Our team will build a Command Line Interface Tool that implements the TURN protocol. This tool will allow users to send and receive data to another computer behind a NAT with a TURN server acting as an intermediary. The actual implementation of the protocol will be given to our customer, Capt Burn, USMC at MARFORCYBER.
  
- **What problem will it solve?**
  
Our product will support MARFORCYBER in their Research and Development needs. Our implementation of the TURN Protocol with authentication and encryption features will support MARFORCYBER in research that they would not be able to do without our work and commitment to the project. Our Command Line Interface will make it so that our customer can easily use our product solo if they choose to do so.

- **Why is it important?**
  
Our product will directly support current research and development needs of MARFORCYBER. The product that our customer is asking for as well as our research done on the TURN protocol and authentication from client to peer(s) is directly supporting the mission of MARFORCYBER. This tool is made to ameliorate a deficiency in utilities that supports the larger MARFORCECYBER mission.

- **High-Level Diagram (OV-1)**

![TURN Net Diagram](TURN_Diagram.png)

## Market Research/Lit Review

- **Existing Processes**
  
Currently the customer has no tool similar to the one we are creating. They have identified TURN as a useful protocol for their R&D needs and require a tool that implements the protocol in a way that is accessible. Our capstone will be delivered to our customer as a CLI tool but our implementation of TURN will be delivered separately for the customer to continue working on it. As of right now our customer will take our tool but it is highly likely that they will use our implementation to add to already existing research.

- **Market Research**

- TURN/STUN

In a typical setting, TURN (Traversal Using Relays around NAT) servers are used to make connections between hosts when the connection to a STUN (Session Traversal Utilities for NAT) server fails. The context in which these servers are typically used is called WebRTC (Web Real-Time Connection), which is a peer-to-peer connection between two web hosts. The STUN and TURN protocols are used by servers in facilitating the “handshake” between the two peers to ensure a connection has been made.  The STUN server will attempt to identify the IPs of each host to connect them, but if that fails, the TURN server is used as a backup. The TURN server does this by relaying information between two parties instead of establishing a direct route for passing information between hosts. In our project, we want to prioritize using the TURN server instead to abstract the source of the connection. 

- Wireguard

Tailscale makes use of the Wireguard protocol, which is an open source encrypted networking protocol. Wireguard is labeled as a general purpose Virtual Private Network that is cross platform and considered an extremely simple, while safe solution to networking needs. The protocol can be implemented in under 4,000 lines of code making it much smaller and faster than OpenVPN or OpenSSL, which are similar services. Wireguard also uses advanced cryptography protocols like the Noise framework, Curve25519, ChaCha20, Poly1305, and more.

Similar to TURN, Wireguard encapsulates IP packets over UDP. The user then adds a simple network interface and configures Wireguard with their private key and their peers public keys. Then the packet transfer process can begin. This process is meant to be as simple and easy to use as SSH. Additionally, Wireguard is extremely lightweight and utilizes lightweight tunnels from the client to each of its peers. When two tailscale clients are behind NATs and a firewall Tailscale falls back on the STUN and ICE protocols to make these connections work.

- Tailscale
  
There are many multimedia applications of the TURN protocol for P2P networking for peers behind NAT. The closest complete solution to this project would be Tailscale. Tailscale is a VPN service that allows any device you own to become accessible anywhere in the world through a secure VPN acting as an intermediary between the two devices.

The goal of our capstone is to provide a very similar product that uses TURN Servers as an intermediary, rather than Virtual Private Networks. Just like Tailscale our product will rely on the the STUN and ICE protocols, which are the foundational layers to the TURN protocol. Although more commercial products are mostly moving towards the use of Virtual Private Networks, TURN servers are still very much in use today. All WebRTC Applications need a server to relay tasks between peers and TURN servers are the primary solution to this is a TURN server. Currently, MARFORCYBER needs research and development work done in this area of networking since the primary focus right now is on VPNs. Our capstone will fill in that gap and directly support the mission of MARFORCYBER.

- **Discovery Insights**
  
In our research we found two primary objectives we need to accomplish. First is implementing the TURN and STUN protocols in accordance with the applicable RFCs. We hope to accomplish this by assembling packets using various python networking libraries like dpkt and scapy. The second objective is to implement a secure authentication method for the protocol. In order to achieve secure authentication we will do research on TLS and Certifications. The final result will simply be a merge of both implementations that should work together seamlessly. Our ultimate goal is that the CLI tool will be operate similar to tools like Metasploit to make the user experience easy and simple to use.

## Proposed Design and Architecture

- **User Types/Personas**
  
Capt Burn is our customer and user. He will use our research and product to supplment his own work at MARFORCYBER. In our primary inteviews with the customer we discussed different user stories and settled on some core elements of our protduct. The plan is to write our product in Python and focus on networking between Linux machines.

- **System Design**
  
Our implementation of the TURN protocol and authentication method will work together seamlessly. From the user's point of view the CLI Tool will be simple and easy to use. Configuration will be akin to configuring an exploit in Metasploit, for example.

- **System Architecture**
  
See OV-1 for an example of the system architecture. No hardware is needed for this capstone as everything will be virtualized.

## Project Management

- **Preliminary Release Plan**

| Sprint | Duration | Start Date | End Date | Goals | Deliverables | Status |
|--------|----------|------------|----------|-------|--------------|--------|
| 1      | 2 weeks  | 2024-10-21 | 2024-11-03 | Set Up Python Environment | Environment Setup for Testing and Development | Finished |
|        |          |            |           | Subitems: | Testing, Libraries, Main | |
| 2      | 3 weeks  | 2024-11-04 | 2024-11-24 | Virtual Box Testing Environment Setup | VyOS Configuration, 5 VMs and 3 Vnets Setup, Terraform | Not Started |
|        |          |            |           | Subitems: | 5vms, 3 Vnets Manual, Terraform, VyOS | |
| 3      | 4 weeks  | 2024-11-25 | 2024-12-22 | Authentication | TLS and Certificates | Not Started |
|        |          |            |           | Subitems: | TLS and Tunneling, Forge Some Certificates!, Server and Client Certificates, Trust Anchor: OpenSSH (python library) | |
| 4      | 2 weeks  | 2024-12-23 | 2024-01-05 | Implement TURN Protocol (Part 1) | Allocate Request, Allocate Response Handling, Refresh Request Handling | Not Started |
|        |          |            |           | Subitems: | Sending an Allocate Request, Receiving an Allocate Request, Receiving an Allocate Success Response, Receiving an Allocate Error Response | |
| 5      | 2 weeks  | 2024-01-06 | 2024-01-19 | Implement TURN Protocol (Part 2) | CreatePermission Request and Response Handling, Send Indication | Not Started |
|        |          |            |           | Subitems: | Sending a Refresh Request, Receiving a Refresh Request, Forming a CreatePermission Request, Receiving a CreatePermission Request, Receiving a CreatePermission Response | |
| 6      | 2 weeks  | 2024-01-20 | 2024-02-02 | Implement TURN Protocol (Part 3) | ChannelBind Request and Response, Data Relaying | Not Started |
|        |          |            |           | Subitems: | Forming a Send Indication, Receiving a Send Indication, Receiving a UDP Datagram, Receiving a Data Indication, Sending a ChannelBind Request, Receiving a ChannelBind Response | |
| 7      | 2 weeks  | 2024-02-03 | 2024-02-16 | Implement TURN Protocol (Part 4) | ChannelData Message Handling | Not Started |
|        |          |            |           | Subitems: | Format ChannelData Message, Sending a ChannelData Message, Receiving a ChannelData Message, Relaying Data from the Peer | |
| 8      | 2 weeks  | 2024-02-17 | 2024-03-01 | Merge Authentication and TURN Protocol | Integration of Authentication and TURN Features | Not Started |
| 9      | 2 weeks  | 2024-03-02 | 2024-03-15 | CLI Tool Development | Basic CLI functionality | Not Started |
| 10     | 1 week   | 2024-03-16 | 2024-03-22 | Documentation | Finishing documentation that was worked on throughout the capstone | Not Started |

- **Product Backlog**

### Priority 1: TURN Protocol Implementation

1. **Implement TURN Protocol (Part 1)**
   - Sending an Allocate Request
   - Receiving an Allocate Request
   - Receiving an Allocate Success Response
   - Receiving an Allocate Error Response
   - Sending a Refresh Request
   - Receiving a Refresh Request

2. **Implement TURN Protocol (Part 2)**
   - Receiving a Refresh Response
   - Forming a CreatePermission Request
   - Receiving a CreatePermission Request
   - Receiving a CreatePermission Response
   - Forming a Send Indication
   - Receiving a Send Indication

3. **Implement TURN Protocol (Part 3)**
   - Receiving a UDP Datagram
   - Receiving a Data Indication
   - Sending a ChannelBind Request
   - Receiving a ChannelBind Response

4. **Implement TURN Protocol (Part 4)**
   - Format ChannelData Message
   - Sending a ChannelData Message
   - Receiving a ChannelData Message
   - Relaying Data from the Peer

### Priority 2: Authentication

1. **TLS and Tunneling**
   - Implement TLS protocols to secure data transmission.
   - Configure and manage tunneling mechanisms for secure communication.

2. **Forge Certificates**
   - Create and validate certificates for secure communication.
   - Ensure server and client certificate validation processes are in place.

3. **Server and Client Certificates**
   - Set up the server and client certificates for secure interactions.
   - Test the certificates' functionality.

4. **Trust Anchor: OpenSSH (Python Library)**
   - Implement OpenSSH library in the authentication flow.
   - Integrate with existing security frameworks.

### Priority 3: Merge Authentication and TURN Protocol

1. **Merge Authentication and TURN Protocol**
   - Integrate Authentication with TURN Protocol functionality.
   - Ensure seamless operation between the Authentication process and TURN server.

### Priority 4: CLI Tool Development

1. **Basic CLI Functionality**
    - Implement core CLI commands to interact with the system.
    - Ensure commands can trigger the main features like TURN and Authentication.
    - Add error handling and user feedback.

### Lower Priority Tasks: Infrastructure Setup & Documentation

1. **Set Up Python Environment**
    - Install and configure necessary libraries for development.
    - Set up environment for testing and main codebase.

2. **Virtual Box Testing Environment Setup**
    - Set up 5 VMs and 3 Vnets.
    - Configure VyOS.
    - Implement infrastructure using Terraform.

3. **Documentation**
    - Consolidate and finalize documentation.
    - Ensure documentation reflects the work done throughout the project.
    - Create guides for installation, setup, and usage.

## **Risk Mitigation**

Complexity of TURN

  - Our research into the protocol must be in depth so we are not surprised by friction in our TURN scrums.
  - Merging of Authentication and TURN.
    - Our implementation of TURN and authentication feature must be able to work together to securely communicate between the client, server, and peer(s).
  
Documentation

  - Each feature must be properly documented for us and our customer.
  - Each part of the TURN protocol builds upon each other so understanding the code that someone else potentially wrote for the previous part is vital to this capstone's success.

Virtual Network

  - Proper set up of our virtual network, as shown in OV-1, will be crucial to the testing of our product.

Testing

  - Every function of every feature must be thoroughly tested.
  - Making use of pytest and other automatic testing suites will ensure that each piece is properly working down the line and that there are no surprises towards the end of the release plan.

## **Key Faculty Involvement**

Networking: LCDR Downs
Authentication: Professor Brown
General Development: Capt Burn (MARFORCYBER)

## Admin/Fine Print

- **GFI/GFE (Government-Furnished Information/Equipment)**
  
None

- **Customer Meeting Requirements/Plan**
  
Outline a meeting schedule or plan for engaging with your customer during development. Highlight key touchpoints for feedback.

- **Acceptance Window**
  
The final version of our Capstone project will be complete by April.

- **Code Delivery**
  
Every version of our Capstone project will be delivered to our customer through our repository every two weeks. Capt Burn is a member of our GitHub repository so he is constantly aware of our progress.

- **Usage License**
  
The software developed as part of the capstone course becomes
property of the DoD. The Computer Science Department does not assume any
responsibility for maintaining the software produced for any customer of the capstone
project. The customer may use the software within the context of their USNA affiliation,
and may not distribute it without approval from the USNA legal office.
