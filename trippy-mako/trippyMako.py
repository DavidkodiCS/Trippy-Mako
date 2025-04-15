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

# ----------------------#
# Trippy-Mako Main Menu #
# ----------------------#
def main():
    ## Welcome Message ##
    try:
        with open("w1.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: Welcome file not found...")
        
    print("Type 'help' to see the available commands or 'exit' to quit...\n\n")
    
    while True:
        configManager = ConfigManager()
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
                turnInfo = configManager.generalSetup()
                if turnInfo == -1:
                    continue
                start_send_file_client(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "listen -f" | "listen -file":
                turnInfo = configManager.generalSetup()
                if turnInfo == -1:
                    continue
                start_file_listener(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "connect": ## get a shell
                turnInfo = configManager.generalSetup()
                if turnInfo == -1:
                    continue
                start_shell_client(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "listen -s" | "listen -shell":
                turnInfo = configManager.generalSetup()
                if turnInfo == -1:
                    continue
                start_shell_listener(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "message":
                turnInfo = configManager.generalSetup()
                if turnInfo == -1:
                    continue
                start_quick_message_client(turnInfo[0], turnInfo[1], turnInfo[2], turnInfo[3])
            case "listen -m" | "listen -message":
                turnInfo = configManager.generalSetup()
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