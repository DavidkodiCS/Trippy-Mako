#!/usr/bin/env python3

#Imports
import configparser
import turnTM

##Command Functions
def help():
    try:
        with open("help.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: Welcome file not found...")  

def config():
    configOptions()
    
    while True:
        command = input("\nconfig > ").strip()
        
        match command:
            case 'exit':
                print("Returning to Home...")
                break             
            case 'create':
                addConfig()
            case 'remove':
                removeConfig()
            case 'edit':
                editConfig()
            case 'list':
                listConfig()
            case 'options':
                configOptions()
            case _:
                print("Unrecognized Command...")

def connect():
    pass

def sendPayload():
    pass

def proxy():
    pass

#Configuration Commands
def addConfig():
    name = input("Enter configuration name: ")
    turnIP = input("Enter TURN server IP address: ")
    turnPort = input("Enter TURN server port number: ")
    protocol = input("Enter desired protocol: ")
    
def removeConfig():
    pass

def editConfig():
    pass

def listConfig():
    print(configuration.sections())

def configOptions():
    print('1. create\n2. remove\n3. edit\n4. list\n5. exit\n')

##Main Functions
def welcome():
        try:
            with open("w1.txt", "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("Error: Welcome file not found...")    
        print("Type help to see the available commands or exit to quit...\n\n")
    
def trippyMako():
    while True:
        command = input("\n> ").strip()
        
        match command:
            case 'exit':
                print("Exiting...")
                break             
            case 'help':
                help()
            case 'config':
                config()
            case 'send':
                sendPayload()
            case 'proxy':
                proxy()
            case _:
                print("Unrecognized Command...")

## MAIN ##
if __name__ == '__main__':
    #User Configurations
    configuration = configparser.ConfigParser()
    configuration.read('configs.ini')
    
    welcome()
    trippyMako()