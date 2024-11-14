# Capstone Proposal

## Overview

**What are you planning to build?**  
Our team will build a Command Line Interface Tool that implements the TURN protocol, using RFC 8656 as our main source of documentation. This project consists of several main parts:

1. Command Line Interface: This tool will allow a user to use several commands such as,

  **configure**: Allows the user to enter in the TURN Server's public facing IP address, associated port number, as well as the user's desired protocol to use, and authentication measures. Different settings could affect the speed and size of the packets being sent across the network, which may be important to the user.

  **connect**: Allows the user to initiate a TCP connection over through the TURN server to establish a more permanent connection a peer, like a secure shell.

  **send**: Allows the user to send a payload using the specified protocol specified in the configuration stage.

  The tool will check the specified configuration during an action and, if it is incorrect, will highlight to the user what is incorrect and will prompt the user to make the changes with suggestions.

2. TURN Implementation:

  Our implementation of the TURN protocol will be derived directly from our research on RFC 8656 and the various RFCs that support TURN to include STUN and the ICE protocol. We will not be using a python library, such as aiortc, due to the requests of our customer. We want the autonomy to implement our own features without being tied to a huge library and build up our **trusted** codebase as we see fit.

This tool will allow users to send and receive data to another computer behind a NAT with a TURN server acting as an intermediary. The actual implementation of the protocol will be provided to our customer, Capt Burn, USMC at MARFORCYBER. Our tool will assist MARFORCYBER in current research and development needs by providing them with a standalone binary that can accomplish this task rather than a library that they would have to implement themselves.

**What problem will it solve?**  
Our product will support MARFORCYBER in their Research and Development needs. Our customer needs a standalone binary, not tied to any major libraries that accomplished the task of allowing a user to utilize the TURN protocol through a CLI in order to send a payload or create a TCP connection that produces a shell, albeit an unconventional use of TURN. Our customer specifically asked for security features such as payload encryption and password protection that would make having our own codebase much more practical than a WebRTC implementation, for example. The CLI tool will make it straightforward for the customer to use independently and expedite current research being done at MARFORCYBER.

**Why is it important?**  
Our product will be directly implemented with current research and development efforts by our customer on launch. Our customer needs a flexible and lightweight product that a WebRTC implementation or Wireguard implementation cannot accomplish due to the need to add special features important to the mission. Our customer is specifically looking for a trusted codebase supports their needs without any extra overhead.

Additionally, our capstone will have a classified portion to it that will include work in the SCIF with our customer to produce extra features relevant to the classified mission set of MARFORCYBER.

**High-Level Diagram (OV-1)**  
![TURN Net Diagram](production_diagram.png)
This diagram depicts a high level overview of how of the TURN protocol works. At the production stage, the client would utilize our CLI tool to easily communicate with a peer through a TURN server on the Internet.

## Market Research/Lit Review

**Existing Processes**  
Currently, our customer does not have any research or development efforts focused on our topic. While TURN has been identified as a useful protocol, a tailored tool that implements it in an accessible way is needed. Although our primary deliverable will be a CLI tool, the TURN protocol implementation will be shared with the customer to integrate into existing research initiatives.

**Market Research**  

**TURN/STUN**  
In typical settings, TURN (Traversal Using Relays around NAT) servers are used when connections to STUN (Session Traversal Utilities for NAT) servers fail. TURN operates in WebRTC (Web Real-Time Communication) environments, acting as a relay when a direct peer-to-peer connection is not possible. The TURN server relays information between peers, bypassing direct host-to-host communication.

**WebRTC**

WebRTC (Real-Time Communication) is an open source project that implements various protocols to include TURN in order to achieve real-time audio and/or video communication from one peer to another. Other uses of WebRTC include streaming video and audio as well as file sharing. WebRTC provides the tools for developers to establish the connection between peers. In other words, the developer still needs to figure out how to implement the library. After the implementation of WebRTC's suite of protocols and API (for javascript) is complete the Real-Time Transport Protocol is used to transmit audio and/or data. 

A WebRTC agent is comprised of many protocols to include ICE, STUN, and TURN. It is an all-encompassing product with the primary purposes of establishing audio and video streams. An implementation of WebRTC is beyond the scope of what our customer is asking for and would not solve the ask of a standalone binary with the flexibility to meet the very specific requirements of the project, which is secure file transfer and a secure TCP connection from client to peer through a TURN server. The difference between our product and WebRTC is that our customer will not need to do any implementation on launch and it is specifically tailored to the needs mentioned above.

- [WebRTC - 1](https://restream.io/learn/what-is/webrtc/)
- [WebRTC - 2](https://webrtcforthecurious.com/docs/01-what-why-and-how/)

**aioRTC**

The aioRTC library on github is a WebRTC implementation and Object RTC API, which is used with WebRTC to make RTC applications for the web. AioRTC essentially WebRTC for the beginner. It simplifies the process of achieving the exchange of audio, video, and data channels. Some features include DTLS key and certificate generation, SCTP implementation sending and receiving of audio and video, data channels, etc. AioRTC functions similarly to the WebRTC API and provides a developer with a suite of Python classes and functions that make it easier for a developer to achieve RTC. We will not use this library to complete our project because it is once again out of the scope of what the customer needs. The goal of this project is not to create a TURN protocol suite but rather tool that allows a user to achieve a secure connection to a peer through a TURN server with the simple configuration of several settings through our CLI.

- [aioRTC](https://github.com/aiortc/aiortc)
- [ORTC](https://ortc.org/)

**Wireguard**  
Tailscale utilizes the Wireguard protocol, known for being lightweight, secure, and cross-platform. Wireguard's concise implementation (under 4,000 lines of code) ensures efficiency and speed compared to alternatives like OpenVPN. It encapsulates IP packets over UDP and uses advanced cryptography like Curve25519 and ChaCha20, offering simplicity comparable to SSH.

**Tailscale**  
Tailscale, a VPN service, securely connects devices globally by acting as an intermediary. Similar to our project, Tailscale falls back on STUN and ICE protocols when establishing connections. Our goal is to develop a TURN-based solution instead, filling MARFORCYBER's current research needs.

**Wireguard and Tailscale**
The main difference between our product and the combination of Tailscale and Wireguard is that we are very explicitly not using VPNs. The need from our customer is to create the desired features of our tool using a TURN server as an intermediary between the client and peer. We did get some inspiration from Tailscale since it provides the user with an interactive shell to the various peers that are associated with the client. We plan on accomplishing this same task through a TURN server, which is not a conventional use of TURN but one that is possible. 

**Discovery Insights**  
Our research highlights two primary objectives: implementing the TURN/STUN protocols per RFCs using Python networking libraries such as `dpkt` and `scapy`, and integrating secure authentication. We will explore TLS and certification processes, ensuring our solution is as seamless as tools like Metasploit.

### Similar Libraries

[Coturn](https://github.com/coturn/coturn)
[RTCTunnel: Building a WebRTC Proxy with Go (explains link below)](https://www.doxsey.net/blog/rtctunnel--building-a-webrtc-proxy-with-go/)
[Network tunnels over WebRTC](https://github.com/rtctunnel/rtctunnel)
[Archived Project for TURN SSH (Directs users to link above)](https://github.com/nobonobo/ssh-p2p)
[Pure Go implementation of the WebRTC API](https://github.com/pion/webrtc)
[gortc (STUN Library)](https://github.com/gortc/stun)

gortc is an implementation of the STUN protocol written in the go language. It supports TURN extensions for TCP allocations as well as the STUN protocol according to the STUN RFC (5389). There is a separate repository for a TURN implementation at gortc/turn that is based on TURN RFC 5766. These implementations essentially facilitate connections with their respective server types. Creating a connection with a TURN server in a similar fashion will be a part of the tool we are making.

[processone (STUN and TURN library for Erlang/Elixir)](https://github.com/processone/stun)

This library is a basic implementation of the STUN and TURN protocols as they work together in the WebRTC context. The STUN server obtains a desired IP of a peer, and the TURN server works on top of that to relay traffic if an IP is unavailable. The library is written in Erlang and requires no external dependencies from other languages to use. We will only be using a TURN server with our tool, so it differs from the classic peer-to-peer use cases that STUN and TURN are typically associated with.

### STUN Overview

[STUN Article on Medium](https://medium.com/@jamesbordane57/stun-server-what-is-session-traversal-utilities-for-nat-8a82d561533a)

This is an article that explains the STUN protocol in a more easily-digestible format. It enumerates a lot of the underlying networking concepts behind STUN, such as what a peer-to-peer connection is, how Network Address Translation works, and the limitation of the number of IPs in existence. It explains what the STUN server does on a step-by-step level to transmit data between peers in a number of different formats, such as UDP and TCP. It also mentions how the TURN and ICE protocols relate. This article is a helpful one-stop-shop other than the RFCs that we can reference as we need to review terms and concepts.

### TURN Overview

[CloudFlare TURN expl ****](https://developers.cloudflare.com/calls/turn/what-is-turn/#:~:text=TURN%20works%20similar%20to%20a,and%20operate%20in%20distinct%20ways.)
[Microsoft Learn on TURN](https://learn.microsoft.com/en-us/openspecs/office_protocols/ms-turn/bf1e2a02-4f6e-4975-b83c-74018546b387)

This is an article on extensions created by Microsoft for the TURN protocol. Along with the technical details on the extension like change tracking and product behavior, it includes a nice explanation of how TURN works, specifically the flow of TURN messages. It also includes an informative section on authentication, which may provide us one option we could use for authenticating payloads. We do not plan to use this extension, but it gives a good framework to go off of when building payloads.

### TURN Implementations/ Real Life Usages

[WebRTC](https://webrtc.org/)
[AnyConnect](https://anyconnect.com/stun-turn-ice/)
[TURN server implemented in Rust](https://crates.io/crates/turn-server)
[eturnal TURN Server](https://eturnal.net/)

### STUN Implementations

[STUNTMAN Tool](https://www.stunprotocol.org/)
[JSTUN Tool](https://jstun.javawi.de/)
[STUN Client](https://www.codeproject.com/Articles/18492/STUN-Client)

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

**Code Delivery** ✅
  
Every version of our Capstone project will be delivered to our customer through our repository every two weeks. Capt Burn is a member of our GitHub repository so he is constantly able to track our progress.

**Usage License** ✅
  
The software developed as part of the capstone course becomes
property of the DoD. The Computer Science Department does not assume any
responsibility for maintaining the software produced for any customer of the capstone
project. The customer may use the software within the context of their USNA affiliation,
and may not distribute it without approval from the USNA legal office.
