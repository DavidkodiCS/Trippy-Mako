# TrippyMako Documentation

## Imports

1. configparser: Used to simplify creating, editing, and removing configurations with .ini files.
2. turnTM: Driver code for the main features of Trippy-Mako (send, listen, etc.)
3. asyncio: Used to establish coroutines and tasks to be completeled in parallel to the main event loop

## Trippy-Mako

### Configurations

Trippy-Mako provides the user with a simple way to create, edit, and remove "configurations" to simplify communication with the TURN Server and eventually a peer. 

Each configuration has a title to remind the user of the configuration and fields for the TURN IP and port as well as the desired protocol, which will be implemented in the future. Also, a peer IP and Port might be added in the future if the user wants to make a connection the same peer over and over again.

```
[turn]
turnip = 127.0.0.1
turnport = 5349     # Secure Port
protocol = TCP
```
```
[turn]
turnip = 127.0.0.1
turnport = 3478     # Standard Port
protocol = TCP
```
