#!/usr/bin/env python3
import configparser

#User Configurations
config = configparser.ConfigParser()
config.read('configs.ini')

##Command Functions
def help():
    try:
        with open("help.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: Welcome file not found...")  
        
def configure():
    pass

def connect():
    pass

def sendPayload():
    pass

def proxy():
    pass




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
        
        if command == 'exit':
            print("Exiting...")
            break
        elif command == 'help':
            help()
        elif command == 'configure':
            configure()
        elif command == 'send':
            sendPayload()
        elif command == 'proxy':
            proxy()
            
        


## MAIN ##
if __name__ == '__main__':
    welcome()
    trippyMako()