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
            case "help":
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
    
    #For when adding and immediately using
    return name
        

## Remove Configuration From File ##
def removeConfig():
    listConfig()
    remove = input("Choose section to remove: ")
    configuration.remove_section(remove)

    with open("configs.ini", 'w') as configfile:
        configuration.write(configfile)
    
    print("Configuration successfully removed!")


## Edit Configuration ##
def editConfig():
    while True:
        listConfig()
        edit = input("Choose configuration to edit: ")
        print("Sections:\nturnIP\nturnPort\nprotocol")
        section = input("Choose section to edit: ")

        match section:
            case "turnIP":
                configuration[edit]['turnIP'] = input("New turnIp: ")
            case "turnPort":
                configuration[edit]['turnPort'] = input("New turnPort: ")
            case "protocol":
                configuration[edit]['protocol'] = input("New protocol: ")
            case _:
                print("Invalid Section...")

        with open("configs.ini", 'w') as configfile:
            configuration.write(configfile)

        cont = input("Would you like to continue editing? (y/n)")
        if cont == "y":
            continue
        elif cont == "n":
            break
    
    print("Configuration successfully edited!")

## Display A Configuration ##  
def displayConfig():
    listConfig()
    display = input("Choose configuration to display: ")
    print("TURN IP: " + configuration[display]['turnIP'])
    print("TURN Port: " + configuration[display]['turnPort'])
    print("Protocol: " + configuration[display]['protocol'])
    
def getConfig(config):
    return [configuration[config]['turnIP'], configuration[config]['turnPort'], configuration[config]['protocol']]    

def listConfig():
    print(configuration.sections())


def configOptions():
    print("> create\n> remove\n> edit\n> list\n> display\n> help\n> exit\n")
    
    
## DEMO OPTION ##
def demo():
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
        demo()
    
    turnTM.sendAllocation(info[0], info[1])
    


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
            case "demo":
                demo()
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
