#!/usr/bin/env python3

## Imports ##
from turnTM import *
from config import *

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
def generalSetup(configManager):
    print("> Choose an existing configuration or create a new one:")
    print("> existing\n> new\n> exit")
    choose = input("Choose: ")
    info = []
    
    if(choose == "existing"):
        if configManager.getNumSections() == 0:
            print("You have no saved configurations.\nPlease create a configuration...\n")
            
            return -1
        print("Please choose a configuration from the list below: ")
        configManager.listConfig()
        config = input("Choose configuration: ")
        if not(configManager.hasSection(config)):
            print("That configuration does not exist.")
            generalSetup(configManager)
        info = configManager.getConfig(config)
          
    elif(choose == "new"):
        config = configManager.addConfig()
        info = configManager.getConfig(config)     

    elif(choose == "exit"):
        return -1

    else:
        print("Invalid command...")
        generalSetup(configManager)
        
    v = input("Would you like to enter verbose mode? (y/n): ")
    info.append(True if v == "y" else False)
    return info

# ----------------------#
# Trippy-Mako Main Menu #
# ----------------------#
def main():
    configManager = ConfigManager()

    ## Welcome Message ##
    try:
        with open("w1.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: Welcome file not found...")
        
    print("Type 'help' to see the available commands or 'exit' to quit...\n\n")
    
    while True:
        command = input("\n> ").strip()             

        match command:
            case "exit":
                print("Exiting...")
                break
            case "help":
                help()
            case "config":
                configManager.config()
            case "proxy":
                print("Feature not implemented yet")
            case "sendFile":
                turnInfo = generalSetup(configManager)
                if turnInfo == -1:
                    continue
                start_send_file_client(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "listen -f" | "listen -file":
                turnInfo = generalSetup(configManager)
                if turnInfo == -1:
                    continue
                start_file_listener(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "connect": ## get a shell
                turnInfo = generalSetup(configManager)
                if turnInfo == -1:
                    continue
                start_shell_client(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "listen -s" | "listen -shell":
                turnInfo = generalSetup(configManager)
                if turnInfo == -1:
                    continue
                start_shell_listener(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "message":
                turnInfo = generalSetup(configManager)
                if turnInfo == -1:
                    continue
                start_quick_message_client(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "listen -m" | "listen -message":
                turnInfo = generalSetup(configManager)
                if turnInfo == -1:
                    continue
                start_message_listener(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case _:
                print("Unrecognized Command...")

################################################################################
################################################################################

## Run Trippy-Mako ##
if __name__ == "__main__":
    main()