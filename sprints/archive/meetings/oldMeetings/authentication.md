# Authentication Notes: Dr. Brown Meeting

- **The Problem**

    1. TLS Solves the problem:
        - Built on top of TCP (I think TURN encapsulates UDP, but we can figure this out later)
        - Authenticated with certificates
        - Encryption
    2. Authentication needed in both directions (server and client)
        - We want to make sure the TURN server is who they say they are
        - We need to tell the TURN server (who will tell the peer) that we are good to go (we will make our own certificates)
    3. TURN RFC
        - TLS/UDP/TCP Tunneling
        - TLS Session
        - Then Normal TLS using port and ip
    4. Build Authentication functionality then simply plop into TURN implementation

- **Other Notes**

  - Look for Python libraries that do TLS(Server and Client) w/ Client and Server Certificates
    - **Trust Anchor**: openSSH? --> be your own Authority!

## What we need to do in a nutshell

    1. Start with making a basic TLS server and client
    2. Add the certification layer to it, which includes being our own authority
    3. ???
