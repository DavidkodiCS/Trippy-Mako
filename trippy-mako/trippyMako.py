#!/usr/bin/env python3

## Imports ##
from turnTM import *
from config import *

# ------------#
# Trippy-Mako #
# ------------#

#------------------#
# Helper Functions #
#------------------#

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
                turnTM = TurnTM(turnInfo)
                
                match command: 
                    case "sendFile":
                        turnTM.start_send_file_client()
                    case "listen -f" | "listen -file":
                        turnTM.start_file_listener()
                    case "connect":
                        turnTM.start_shell_client()
                    case "listen -s" | "listen -shell":
                        turnTM.start_shell_listener()
                    case "message":
                        turnTM.start_quick_message_client()
                    case "listen -m" | "listen -message":
                        turnTM.start_message_listener()
                    case _:
                        print("Unrecognized Command...")

################################################################################
################################################################################

## Run Trippy-Mako ##
if __name__ == "__main__":
    main()