# Sprint 4/5 Report  

## Features Developed and Demoed During the Sprint Review  

### Sprint 4  

1. As a user, I can demonstrate communication between two hosts and a TURN server on the same LAN.  
2. As a user, I can send Allocation and Refresh packets to the TURN server from a private network (behind a NAT).  
3. R&D: Testing Architecture Pt. 2.  
4. As a user, I can listen for another peer to send me data.  

### Sprint 5  

1. As a user, I can enter a peer's IP address and port into a configuration.  
2. As a user, I can send messages and files to a peer via the TURN server.  
3. As a user, I can initiate a TCP connection with a peer and gain remote access.  
4. Complete issue backlog refinement and development/user documentation.  
5. As a developer, I can spin up an EC2 instance with Coturn to test with VNets.  

## Accepted Features  

All features for this sprint have been tentatively accepted after the demo, which encompasses Sprints 4 and 5. Once we successfully demonstrate peer-to-peer communication, all features will be considered 100% complete.  

## Stories/Features Added to the Backlog Since the Last Sprint Review  

**Feature 1:** As a user, I can use all three main features of Trippy-Mako to communicate with a peer.  

We had to push all features related to client-peer communication to the next sprint due to significant blockers. These features have been consolidated into a single feature for the next sprint, as resolving this issue will ensure all core functionalities work as intended.  

## Updates to the Release Plan  

Authentication and encryption will be pushed back to Sprint 7 so we can focus on establishing client-peer communication, allowing us to complete all the main features of Trippy-Mako.  

### [Updated Member Velocities](https://docs.google.com/spreadsheets/d/1iDczfXFm2CANtSYXumhWK-F_ozv4bLBBos8dFoWCZYU/edit?gid=1321373368#gid=1321373368)  

## [Next Sprint Plan](https://docs.google.com/spreadsheets/d/1iDczfXFm2CANtSYXumhWK-F_ozv4bLBBos8dFoWCZYU/edit?gid=601765542#gid=601765542)  

In the next sprint, we need to overcome the major blocker from the past two sprints: ensuring proper communication between our client and peer using the TURN server hosted on an AWS EC2 instance.