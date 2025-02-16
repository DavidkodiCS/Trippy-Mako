#!/usr/bin/env python3

## Imports ##
import configparser
import turnTM
import os
import asyncio


## Command Functions ##
def help():
    try:
        with open("help.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: Welcome file not found...")

## Secure TCP Connection (Shell) ##
def connect():
    pass

## Feature to send messages and larger payloads to a peer ##
def sendPayload():
    print("> Choose an existing configuration or create a new one:")
    print("> existing\n> new")
    choose = input("Choose: ")
    info = []
    
    if(choose == "existing"):
        print("Please choose a configuration from the list below: ")
        listConfig()
        config = input("Choose configuration: ")
        info = getConfig(config)
          
    elif(choose == "new"):
        config = addConfig()
        info = getConfig(config)     

    else:
        print("Invalid command...")
        sendPayload()
    
    asyncio.run(turnTM.start_send_client(info[0], info[1]))


def proxy():
    pass

## LISTEN ##
def listen():
    print("> Choose an existing configuration or create a new one:")
    print("> existing\n> new")
    choose = input("Choose: ")
    info = []
    
    if(choose == "existing"):
        print("Please choose a configuration from the list below: ")
        listConfig()
        config = input("Choose configuration: ")
        info = getConfig(config)
        
    elif(choose == "new"):
        ##For current demo
        ##IP = 127.0.0.1
        ##PORT = 5349
        config = addConfig()
        info = getConfig(config)     
    else:
        print("Invalid command...")
        listen()
    
    asyncio.run(turnTM.start_listener_client(info[0], info[1]))
    
## DEMO OPTION ##
# def demo():
#     print("> Choose an existing configuration or create a new one:")
#     print("> existing\n> new")
#     choose = input("Choose: ")
#     info = []
    
#     if(choose == "existing"):
#         print("Please choose a configuration from the list below: ")
#         listConfig()
#         config = input("Choose configuration: ")
#         info = getConfig(config)
        
#     elif(choose == "new"):
#         ##For current demo
#         ##IP = 127.0.0.1
#         ##PORT = 5349
#         config = addConfig()
#         info = getConfig(config)     
#     else:
#         print("Invalid command...")
#         demo()
    
#     asyncio.run(turnTM.start_client(info[0], info[1]))

## Configuration Menu ##
def config():
    print("Configuration Menu")
    configOptions()

    while True:
        command = input("\nconfig > ").strip()

        match command:
            case "exit":
                print("Returning to Home...")
                break
            case "create":
                addConfig()
            case "remove":
                removeConfig()
            case "edit":
                editConfig()
            case "list":
                listConfig()
            case "help":
                configOptions()
            case "display":
                displayConfig()
            case _:
                print("Unrecognized Command...")
                
## Configuration Commands ##

## Add configuration to configs.ini ##
def addConfig():
    name = input("Enter configuration name: ")
    
    ## search for the entered name and notify the user if it already exists ##
    while configuration.has_section(name):
        print("Configuration name already exists.\nWould you like to 'edit' the existing config or 'create' a new one?")
        command = input("config > ")
        match command:
            case "edit":
                editConfig()
                return
            case "create":
                name = input("Enter configuration name: ")
            case _:
                print("Unrecognized command...")
            

    ## Enter in fields about server configuration ##
    turnIP = input("Enter TURN server IP address: ")
    turnPort = input("Enter TURN server port number: ")
    protocol = input("Enter desired protocol: ")

    # add configuration to the file 
    configuration.add_section(name)
    configuration[name]['turnIP'] = turnIP
    configuration[name]['turnPort'] = turnPort
    configuration[name]['protocol'] = protocol

    with open(config_path, 'w') as configfile:
        configuration.write(configfile)
    
    print("Configuration successfully added!")
    
    # For when adding and immediately using
    return name
        

## Remove Configuration From configs.ini ##
def removeConfig():
    listConfig()
    section = input("Choose section to remove: ")
    
    if configuration.has_section(section):
        configuration.remove_section(section)

        with open("configs.ini", 'w') as configfile:
            configuration.write(configfile)
        
        print("Configuration successfully removed!")
    else:
        print("Section does not exist...")

## Edit Configuration ##
def editConfig():
    listConfig()
    section = input("Choose configuration to edit: ")
    
    if configuration.has_section(section):
        print("Sections:\n\tturnIP\n\tturnPort\n\tprotocol")
        
        while True:
            field = input("Choose field to edit: ")

            match field:
                case "turnIP":
                    configuration[section]['turnIP'] = input("New turnIp: ")
                case "turnPort":
                    configuration[section]['turnPort'] = input("New turnPort: ")
                case "protocol":
                    configuration[section]['protocol'] = input("New protocol: ")
                case _:
                    print("Invalid Field...")

            ## Write to configs.ini
            with open("configs.ini", 'w') as configfile:
                configuration.write(configfile)

            cont = input("Would you like to continue editing? (y/n)")
            if cont == "y":
                continue
            elif cont == "n":
                break
    
        print("Configuration successfully edited!")
    else:
        print("Section does not exist...")

## Display Configuration Fields ##  
def displayConfig():
    listConfig()
    display = input("Choose configuration to display: ")
    if configuration.has_section(display):
        print("TURN IP: " + configuration[display]['turnIP'])
        print("TURN Port: " + configuration[display]['turnPort'])
        print("Protocol: " + configuration[display]['protocol'])
    else:
        print("Section does not exist...")
    
## Returns array containing all of the chosen configurations fields ##
def getConfig(config):
    return [configuration[config]['turnIP'], configuration[config]['turnPort'], configuration[config]['protocol']]    

## Lists the configuration names currently in config.ini ##
def listConfig():
    print(configuration.sections())

## Options ##
def configOptions():
    print("> create\n> remove\n> edit\n> list\n> display\n> help\n> exit\n")

### Trippy-Mako Main Menu###
def main():
    ## Load Configuration File ##
    global configuration
    global config_path
    configuration = configparser.ConfigParser()
    configuration.read("configs.ini")
    
    # Get config directory from environment variable
    config_dir = os.getenv("CONFIG_DIR", "/config")
    config_path = os.path.join(config_dir, "settings.ini")
    os.makedirs(config_dir, exist_ok=True)

    # Read existing configurations if the file exists
    if os.path.exists(config_path):
        configuration.read(config_path)

    ## Welcome Message ##
    try:
        with open("w1.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: Welcome file not found...")
        
    print("Type help to see the available commands or exit to quit...\n\n")
    
    while True:
        command = input("\n> ").strip()

        match command:
            case "exit":
                print("Exiting...")
                break
            case "help":
                help()
            case "config":
                config()
            case "send":
                sendPayload()
            case "proxy":
                proxy()
            case "listen":
                listen()
            case _:
                print("Unrecognized Command...")

################################################################################
################################################################################

## Run Trippy-Mako ##
if __name__ == "__main__":
    main()