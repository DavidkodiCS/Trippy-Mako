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
def print_help():
    try:
        with open("help.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: Welcome file not found...")
        
## Welcome Message ##
def welcome():
    try:
        with open("w1.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: Welcome file not found...")

# ----------------------#
# Trippy-Mako Main Menu #
# ----------------------#
def main():
    welcome()
    print("Type 'help' to see the available commands or 'exit' to quit...\n\n")
    
    configManager = ConfigManager()
    while True:
        
        command = input("\n> ").strip()             

        match command:
            case "exit":
                print("Exiting...")
                break
            case "help":
                print_help()
            case "config":
                configManager.config()
            case _:
                ## SET UP ##
                turnInfo = configManager.generalSetup()
                if turnInfo == None:
                    continue
                
                match command: 
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