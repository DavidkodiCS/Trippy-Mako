# Trippy-Mako

Capstone Project USNA 2025

## Team

David Kreidler, Meris Larkins, Charlie Francesconi

## Topic

TURN Protocol Command Line Interface Tool

## What It Does

Trippy-Mako is a command-line tool that allows a host to securely communicate with another host, both of which are behind NAT networks, without connecting to each other. It does this by interfacing with a TURN (Traversal Using Relays around NAT) Server, and there are multiple specific functions Trippy-Mako uses to do so:

configure: Allows the user to enter in the TURN Server's public facing IP address, 
associated port number, as well as the user's desired protocol to use, and 
authentication measures. Different settings could affect the speed and size of 
the packets being sent across the network, which may be important to the user.

connect: Allows the user to initiate a TCP connection over through the TURN 
server to establish a more permanent connection a peer, like a secure shell.

send: Allows the user to send a payload using the specified protocol specified 
in the configuration stage.

The tool will check the specified configuration during an action and, if it is 
incorrect, will highlight to the user what is incorrect and will prompt the user 
to make the changes with suggestions.

proxy: Using this command will allow the user to create what is essentially an 
open tunnel to the peer through the TURN server to send data through that the peer 
will then send to other devices in the network. The tool will listen on a port and 
provide an interface for the user to send the payload through the tunnel.

listen: This feature allows the client to listen for a peer on the TURN server.

## To Install/Run

### User Run:

1. Navigate to a file where you would like to store configurations
2. run command `docker run -it -v "$(pwd):/config" chazzconi/trippy-mako bash`

### Dev Installation:

1. Clone the repository
2. Within the repository use command `docker build -t trippy-mako .`

### To run:

1. Start Docker Desktop
2. Navigate to a file to save configurations
3. In a terminal run `docker run -it -v "$(pwd):/config" trippy-mako bash`

## Contents

1. [Team Charter](https://github.com/DavidkodiCS/Trippy-Mako/blob/main/Charter.md)
2. [Capstone Proposal](Trippy-Mako/proposal/proposal.md)
3. [TM Style Guide](https://github.com/DavidkodiCS/Trippy-Mako/blob/main/Trippy-Mako-StyleGuide.md)
4. [Literary Review and Brainstorming](https://docs.google.com/document/d/1IeNRIVarfN5WBRGMrVxdDZGXDCPgenVMWErjJEkWA20/edit?usp=sharing)
5. [Poster](https://docs.google.com/presentation/d/1Ua0MMuqRZ-b5kbvC48WoUsahLcg4EEjAxT-er4XbvGA/edit?usp=sharing)
6. [Capstone Presentation](https://docs.google.com/presentation/d/1EEil-rpdahq-6Y4z7Y-bLYhUQXilDrPkDXivoDhVkWI/edit?pli=1#slide=id.g32576c3bf74_0_346)
