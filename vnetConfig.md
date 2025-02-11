## How to set up the virtual network for testing:

# 1. Create VMs
- TURN Server VM: A host of any OS that is running Coturn and has one network interface (leave as NAT)
- Host VMs: Hosts of any OS that have one network interface each (each has its own internal network)
- Router VMs: Two hosts running PfSense (installation tutorial linked below) that each have two network interfaces: one on the internal network of its respective host and one left as NAT

# 2. Download and Install PfSense
- Download the ISO file from the PfSense website (it's specifically for installing on a VM)
- Follow this YouTube tutorial for initial installation/configuration: [link](https://www.youtube.com/watch?v=dFsjB03_9jQ)
- Navigate to the web configuration tool using the URL you generate after configuring your interfaces on the host within the same internal network
- Go to Services -> DNS Resolver and turn on forwarding. You will likely not be connected to the Internet otherwise
- If you still don't have Internet, go to Firewall -> Rules and make rules allowing traffic to port 53 for TCP and UDP

# 3. Install and Configure Coturn on the TURN Server VM
