#!/usr/bin/env python3

## Imports ##
import configparser
from turnTM import *
import os

# ------------#
# Trippy-Mako #
# ------------#

# -----------------------#
# Main Command Functions #
# -----------------------#

## Display Help ##
def help():
    try:
        with open("help.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: Welcome file not found...")

## General Config Setup for Main Features ##
def generalSetup():
    print("> Choose an existing configuration or create a new one:")
    print("> existing\n> new\n> exit")
    choose = input("Choose: ")
    info = []
    
    if(choose == "existing"):
        if len(configuration.sections()) == 0:
            print("You have no saved configurations.\nPlease create a configuration...\n")
            
            return -1
        print("Please choose a configuration from the list below: ")
        listConfig()
        config = input("Choose configuration: ")
        if not(configuration.has_section(config)):
            print("That configuration does not exist.")
            generalSetup()
        info = getConfig(config)
          
    elif(choose == "new"):
        config = addConfig()
        info = getConfig(config)     

    elif(choose == "exit"):
        return -1

    else:
        print("Invalid command...")
        generalSetup()
        
    v = input("Would you like to enter verbose mode? (y/n): ")
    info.append(True if v == "y" else False)
    return info
                
# -----------------------#
# Configuration Commands #
# -----------------------#

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
    encrypt = input("Encrypted? (y/n ): ")

    # add configuration to the file 
    configuration.add_section(name)
    configuration[name]['turnIP'] = turnIP
    configuration[name]['turnPort'] = turnPort
    configuration[name]['encrypted'] = True if encrypt == "y" else False

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
        print("Sections:\n\tturnIP\n\tturnPort\n\encrypted")
        
        while True:
            field = input("Choose field to edit: ")

            match field:
                case "turnIP":
                    configuration[section]['turnIP'] = input("New turnIp: ")
                case "turnPort":
                    configuration[section]['turnPort'] = input("New turnPort: ")
                case "encrypted":
                    configuration[section]['encrypted'] = True if input("Encrypted? (y/n ): ") == "y" else False
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
        print("Encrypted: " + configuration[display]['encrypted'])
    else:
        print("Section does not exist...")
    
## Returns array containing all of the chosen configurations fields ##
def getConfig(config):
    return [configuration[config]['turnIP'], configuration[config]['turnPort'], configuration[config]['encrypted']]    

## Lists the configuration names currently in config.ini ##
def listConfig():
    print(configuration.sections())

## Options ##
def configOptions():
    print("> create\n> remove\n> edit\n> list\n> display\n> help\n> exit\n")

# ----------------------#
# Trippy-Mako Main Menu #
# ----------------------#
def main():
    ## Load Configuration File ##
    global configuration
    global config_path
    configuration = configparser.ConfigParser()
    
    # Get config directory from environment variable
    config_dir = os.getenv("CONFIG_DIR", "/config")
    config_path = os.path.join(config_dir, "config.ini")
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
        
    print("Type 'help' to see the available commands or 'exit' to quit...\n\n")
    
    while True:
        command = input("\n> ").strip()
        if command == "exit":
                print("Exiting...")
                break            
        turnInfo = generalSetup()
        if turnInfo == -1:
            continue
        
        match command:
            case "help":
                help()
            case "config":
                config()
            case "proxy":
                print("Feature not implemented yet")
            case "sendFile":
                start_send_file_client(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "listen -f" | "listen -file":
                start_file_listener(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "connect": ## get a shell
                start_shell_client(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "listen -s" | "listen -shell":
                start_shell_listener(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "message":
                start_quick_message_client(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "listen -m" | "listen -message":
                start_message_listener(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case _:
                print("Unrecognized Command...")

################################################################################
################################################################################

## Run Trippy-Mako ##
if __name__ == "__main__":
    main()