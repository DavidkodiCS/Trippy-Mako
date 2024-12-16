#!/usr/bin/env python3

## Imports ##
import configparser
import turnTM

## Command Functions ##
def help():
    try:
        with open("help.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: Welcome file not found...")


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
            case "options":
                configOptions()
            case "display":
                displayConfig()
            case _:
                print("Unrecognized Command...")


def connect():
    pass


def sendPayload():
    pass


def proxy():
    pass


## Configuration Commands ##
def addConfig():
    name = input("Enter configuration name: ")
    
    # search for the entered name and notify the 
    # user if it already exists
    while configuration.has_section(name):
        print("Configuration name already exists.\nWould you like to 'edit' the existing config or 'create' a new one?")
        command = input("config > ")
        if(command == 'edit'):
            editConfig()
            return
        elif command == 'create':
            name = input("Enter configuration name: ")

    # enter other details about server configuration    
    turnIP = input("Enter TURN server IP address: ")
    turnPort = input("Enter TURN server port number: ")
    protocol = input("Enter desired protocol: ")

    # add configuration to the file 
    configuration.add_section(name)
    configuration[name]['turnIP'] = turnIP
    configuration[name]['turnPort'] = turnPort
    configuration[name]['protocol'] = protocol
    
    with open("configs.ini", 'w') as configfile:
        configuration.write(configfile)
    
    print("Configuration successfully added!")
        

## Remove Configuration From File ##
def removeConfig():
    listConfig()
    remove = input("Choose section to remove: ")
    configuration.remove_section(remove)
    
    print("Configuration successfully removed!")


##NOT DONE YET##
def editConfig():
    listConfig()
    edit = input("Choose section to edit: ")
    
    configuration[edit]['turnIP'] = turnIP
    configuration[edit]['turnPort'] = turnPort
    configuration[edit]['protocol'] = protocol
    
    print("Configuration successfully edited!")

## Display A Configuration ##  
def displayConfig():
    listConfig()
    display = input("Choose configuration to display: ")
    print("TURN IP: " + configuration[display]['turnIP'])
    print("TURN Port: " + configuration[display]['turnPort'])
    print("Protocol: " + configuration[display]['protocol'])


def listConfig():
    print(configuration.sections())


def configOptions():
    print("> create\n> remove\n> edit\n> list\n> display\n> exit\n")


## Main Functions ##
def welcome():
    try:
        with open("w1.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: Welcome file not found...")
    print("Type help to see the available commands or exit to quit...\n\n")

## Main Menu ##
def trippyMako():
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
            case _:
                print("Unrecognized Command...")

## Load Configuration File ##
def configSetup():
    # User Configurations
    global configuration
    configuration = configparser.ConfigParser()
    configuration.read("configs.ini")

## MAIN ##
def main():
    configSetup()
    welcome()
    trippyMako()

## Run Main Function ##
if __name__ == "__main__":
    main()
