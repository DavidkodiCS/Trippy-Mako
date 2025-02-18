# Configuring Coturn on an EC2 instance (AWS)

## AWS Configurations

1. Your AWS EC2 instance should have a security group with the following INBOUND rules(Protocol : Port):
- TCP : 3478
- UDP : 3478
- TCP : 5349
- UDP : 5349

Port 3478 is used for standard TCP/UDP whereas port 5349 is used for when a TLS connection is needed.

2. Configure Network ACL if needed: 
- Your AWS EC2 instance should have a VPC ID in the details section. 
- Click on this and navigate to the main network ACL by clicking on its ID.
- After clicking on the ID again you should see the inbound rules.
- Add the same inbound rules as the security group above.

## EC2 Instance Coturn Configuration

1. Download dependencies:
- sudo yum groupinstall "Development Tools" -y 
- sudo yum install -y libevent-devel gcc make automake autoconf openssl-devel
- sudo yum install -y git

2. Pull coturn from github
- git clone https://github.com/coturn/coturn.git

3. Make Coturn
- cd coturn
- ./configure
- make
- sudo make install

4. Configure turnserver.conf with these attributes:
```
fingerprint
no-auth
no-tls
no-dtls

listening-port=3478
realm=turnserver
listening-ip=0.0.0.0            ## Listen on all interfaces
relay-ip=X.X.X.X                ## EC2 instance public IP
external-ip=X.X.X.X/X.X.X.X     ## PublicIP/PrivateIP
```

5. Run the turn server:
- cd coturn
- sudo turnserver -c turnserver.conf -v

## Still not working?

1. Ensure that your EC2 instance firewall is configured to allow the TURN ports INBOUND and OUTBOUND. 
```
sudo iptables -I INPUT -p udp --dport 3478 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 3478 -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo iptables -I INPUT -p udp --dport 49152:65535 -j ACCEPT
sudo iptables -I OUTPUT -p udp --sport 3478 -j ACCEPT
sudo iptables -I OUTPUT -p tcp --sport 3478 -j ACCEPT
sudo iptables-save | sudo tee /etc/sysconfig/iptables
```
- IF using secure protocols you must all add INBOUND/OUTPUT rules for port 5349.

2. After making changes kill the turn server process and restart:
- sudo pkill turnserver  # Kill running instance