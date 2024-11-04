# Capstone Proposal

## Overview

**What are you planning to build?**  
Our team will build a Command Line Interface Tool that implements the TURN protocol. This tool will allow users to send and receive data to another computer behind a NAT with a TURN server acting as an intermediary. The actual implementation of the protocol will be provided to our customer, Capt Burn, USMC at MARFORCYBER.

**What problem will it solve?**  
Our product will support MARFORCYBER in their Research and Development needs. By implementing the TURN Protocol with authentication and encryption features, we will enable MARFORCYBER to conduct research that would otherwise be difficult to achieve. The CLI tool will make it straightforward for the customer to use independently.

**Why is it important?**  
Our product directly supports MARFORCYBER's ongoing research and development needs. The tool and accompanying research on the TURN protocol and secure client-to-peer authentication will advance MARFORCYBER's mission, addressing current deficiencies in supporting utilities.

**High-Level Diagram (OV-1)**  
![TURN Net Diagram](production_diagram.png)

## Market Research/Lit Review

**Existing Processes**  
Currently, there is no tool similar to what we are creating for the customer. While TURN has been identified as a useful protocol, a tailored tool that implements it in an accessible way is needed. Although our primary deliverable will be a CLI tool, the TURN protocol implementation will be shared with the customer to integrate into existing research initiatives.

**Market Research**  
**TURN/STUN**  
In typical settings, TURN (Traversal Using Relays around NAT) servers are used when connections to STUN (Session Traversal Utilities for NAT) servers fail. TURN operates in WebRTC (Web Real-Time Communication) environments, acting as a relay when a direct peer-to-peer connection is not possible. The TURN server relays information between peers, bypassing direct host-to-host communication.

**Wireguard**  
Tailscale utilizes the Wireguard protocol, known for being lightweight, secure, and cross-platform. Wireguard's concise implementation (under 4,000 lines of code) ensures efficiency and speed compared to alternatives like OpenVPN. It encapsulates IP packets over UDP and uses advanced cryptography like Curve25519 and ChaCha20, offering simplicity comparable to SSH.

**Tailscale**  
Tailscale, a VPN service, securely connects devices globally by acting as an intermediary. Similar to our project, Tailscale falls back on STUN and ICE protocols when establishing connections. Our goal is to develop a TURN-based solution instead, filling MARFORCYBER's current research needs.

**Discovery Insights**  
Our research highlights two primary objectives: implementing the TURN/STUN protocols per RFCs using Python networking libraries such as `dpkt` and `scapy`, and integrating secure authentication. We will explore TLS and certification processes, ensuring our solution is as seamless as tools like Metasploit.

## Proposed Design and Architecture

**User Types/Personas**  
Capt Burn, our customer, will use the tool to support MARFORCYBER's operations. Through interviews, we defined user stories and determined that the tool should be developed in Python, targeting Linux systems for peer-to-peer networking.

**System Design**  
The CLI tool will present a simple configuration interface, drawing on usability parallels with Metasploit. Our TURN protocol implementation will be tightly integrated with authentication to ensure cohesive functionality.

**System Architecture**  
The test architecture is visualized in the detailed diagram below:  
![TURN Test Net Diagram](TURN_Diagram.png)

## Project Management

### Preliminary Release Plan

| Sprint | Duration | Start Date | End Date | Goals | Deliverables | Status |
|--------|----------|------------|----------|-------|--------------|--------|
| 1      | 2 weeks  | 2024-10-21 | 2024-11-03 | Set Up Python Environment | Environment Setup for Testing and Development | Finished |
|        |          |            |           | Subitems: Testing, Libraries, Main | | |
| 2      | 3 weeks  | 2024-11-04 | 2024-11-24 | Virtual Box Testing Environment Setup | VyOS Configuration, 5 VMs and 3 Vnets Setup, Terraform | Not Started |
|        |          |            |           | Subitems: 5 VMs, 3 Vnets Manual, Terraform, VyOS | | |
| 3      | 4 weeks  | 2024-11-25 | 2024-12-22 | Authentication | TLS and Certificates | Not Started |
|        |          |            |           | Subitems: TLS and Tunneling, Forge Certificates, Server and Client Certificates, Trust Anchor: OpenSSH (Python library) | | |
| 4      | 2 weeks  | 2024-12-23 | 2024-01-05 | Implement TURN Protocol (Part 1) | Allocate Request/Response Handling, Refresh Request Handling | Not Started |
|        |          |            |           | Subitems: Sending/Receiving Allocate Requests and Responses | | |
| 5      | 2 weeks  | 2024-01-06 | 2024-01-19 | Implement TURN Protocol (Part 2) | CreatePermission Request/Response Handling, Send Indication | Not Started |
|        |          |            |           | Subitems: Refresh Request Handling, CreatePermission Handling | | |
| 6      | 2 weeks  | 2024-01-20 | 2024-02-02 | Implement TURN Protocol (Part 3) | ChannelBind Request/Response, Data Relaying | Not Started |
|        |          |            |           | Subitems: Send/Receive Indications, UDP Datagram Handling | | |
| 7      | 2 weeks  | 2024-02-03 | 2024-02-16 | Implement TURN Protocol (Part 4) | ChannelData Message Handling | Not Started |
|        |          |            |           | Subitems: Formatting and Relaying ChannelData Messages | | |
| 8      | 2 weeks  | 2024-02-17 | 2024-03-01 | Merge Authentication and TURN Protocol | Integration of Authentication and TURN Features | Not Started |
| 9      | 2 weeks  | 2024-03-02 | 2024-03-15 | CLI Tool Development | Basic CLI Functionality | Not Started |
| 10     | 1 week   | 2024-03-16 | 2024-03-22 | Documentation | Finalize Documentation from Capstone Work | Not Started |

### Product Backlog

**Priority 1: TURN Protocol Implementation**

**Implement TURN Protocol (Part 1)**  

- Sending an Allocate Request
- Receiving an Allocate Request
- Receiving an Allocate Success/Failure Response
- Sending/Receiving a Refresh Request

**Implement TURN Protocol (Part 2)**

- Receiving a Refresh Response
- Creating/Receiving CreatePermission Requests and Responses
- Sending/Receiving Indications

**Implement TURN Protocol (Part 3)**  
- Handling UDP Datagrams and Data Indications
- Sending/Receiving ChannelBind Requests and Responses

**Implement TURN Protocol (Part 4)**

- Formatting ChannelData Messages
- Sending/Receiving ChannelData Messages
- Relaying Peer Data

**Priority 2: Authentication**

**TLS and Tunneling**  

- Implement TLS for secure data transmission
- Configure tunneling for communication security

**Forge Certificates**  

- Create/validate server and client certificates

**Server and Client Certificates**  

- Configure and test certificate functionality

**Trust Anchor: OpenSSH (Python Library)**  

- Integrate OpenSSH in the authentication flow

**Priority 3: Merge Authentication and TURN Protocol**

**Merge Authentication and TURN Protocol**  

- Integrate authentication with TURN protocol
- Ensure cohesive operation between components

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

**Networking:** LCDR Downs

**Authentication:** Professor Brown

**General Development:** Capt Burn (MARFORCYBER)

## Admin/Fine Print

**GFI/GFE (Government-Furnished Information/Equipment)**
  
None

**Customer Meeting Requirements/Plan**
  
Outline a meeting schedule or plan for engaging with your customer during development. Highlight key touchpoints for feedback.

**Acceptance Window**
  
The final version of our Capstone project will be complete by April.

**Code Delivery**
  
Every version of our Capstone project will be delivered to our customer through our repository every two weeks. Capt Burn is a member of our GitHub repository so he is constantly aware of our progress.

**Usage License**
  
The software developed as part of the capstone course becomes
property of the DoD. The Computer Science Department does not assume any
responsibility for maintaining the software produced for any customer of the capstone
project. The customer may use the software within the context of their USNA affiliation,
and may not distribute it without approval from the USNA legal office.
