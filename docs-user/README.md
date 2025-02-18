# User Documentation

## User Guide to running Trippy-Mako:

1. Start Docker Desktop
2. Navigate to a file that you would want to save configurations on
3. In a terminal run `docker run -it -v "$(pwd):/config" trippy-mako bash`

## Creating Configurations

When running Trippy Mako enter: config

Configuration Options:
```
> create : Allows the user to specify the public IP and port of the TURN server and add a new named section to configs.ini.
> remove : Allows the user to remove a configuration from the configs.ini file.
> edit : Allows the user to make changes to existing configurations.
> list : Lists all existing configurations.
> display : Allows the user to select an existing configuration and display its field values.
> help : Displays the configuration commands.
> exit : Exits to the main menu of Trippy Mako.
```

## Feautures

### Send Client

### Send Listener

### Get Shell Client

### Shell Listener Client