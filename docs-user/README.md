# User Documentation

## User Guide to running Trippy-Mako:

1. Start Docker Desktop
2. Navigate to a file that you would want to save configurations on
3. In a terminal run `docker run -it -v "$(pwd):/config" trippy-mako bash`

## Creating Configurations

When running Trippy Mako enter: config

Configuration Options:
```
> create : Allows you to specify the public IP and port of the TURN server and add a new named section to configs.ini.
> remove : Allows you to remove a configuration from the configs.ini file.
> edit : Allows you to make changes to existing configurations.
> list : Lists all existing configurations.
> display : Allows you to select an existing configuration and display its field values.
> help : Displays the configuration commands.
> exit : Exits to the main menu of Trippy Mako.
```

## Feautures

### Send Client

With this feature you can send files to a peer through the TURN server similar to what the SFTP(Secure File Transport Protocol) does.

### Send Listener

With this feature you can connect to a TURN server and wait for incoming files from a peer.

### Get Shell Client

With this feature you can connect to a peer and receive a reverse shell to execute commands on the peer's machine similar to what ssh does.

### Shell Listener Client

With this feature you can connect to a TURN server and wait for an incoming connection from a peer.