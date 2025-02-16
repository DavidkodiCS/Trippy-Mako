## Coturn Testing Document

### [Coturn Github Repository](https://github.com/coturn/coturn)

### Local Testing Setup

#### 1. Install Coturn

sudo apt update
sudo apt install coturn

#### 2. TURN Server Configuration (BASIC)

sudo nano /etc/turnserver.conf

**No authentication and UDP only add the following fields in the configuration file**
listening-port=5349
fingerprint

no-auth

no-tls
no-dtls
no-tcp-relay

#### 3. Run Server

sudo turnserver -c /etc/turnserver.conf -v

#### 4. Sending Packets

python trippyMako.py

1. Use the demo feature for initial testing

### Automating Testing

Testing can be automated by collecting the hex response from the TURN server. A lot of information can be gathered from this response such as success or failure codes. 