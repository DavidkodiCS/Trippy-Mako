# -----------------------#
# Configuration Commands #
# -----------------------#
import configparser
import os

class ConfigManager:
    def __init__(self, path="configs.ini"):
        self.path = path
        
        ## Load Configuration File ##
        global configuration
        global config_path
        self.configuration = configparser.ConfigParser()
        
        # Get config directory from environment variable
        config_dir = os.getenv("CONFIG_DIR", "/config")
        config_path = os.path.join(config_dir, "config.ini")
        os.makedirs(config_dir, exist_ok=True)

        # Read existing configurations if the file exists
        if os.path.exists(config_path):
            self.configuration.read(config_path)
            
    ## General Config Setup for Main Features ##
    def generalSetup(self):
        print("> Choose an existing configuration or create a new one:")
        print("> existing\n> new\n> exit")
        choose = input("Choose: ")
        info = []
        
        if(choose == "existing"):
            if self.getNumSections() == 0:
                print("You have no saved configurations.\nPlease create a configuration...\n")
                self.generalSetup()
                    
            print("Please choose a configuration from the list below: ")
            self.listConfig()
            config = input("Choose configuration: ")
            if not(self.hasSection(config)):
                print("That configuration does not exist.")
                self.generalSetup()
            info = self.getConfig(config)
            
        elif(choose == "new"):
            config = self.addConfig()
            info = self.getConfig(config)     

        elif(choose == "exit"):
            return -1

        else:
            print("Invalid command...")
            self.generalSetup()
            
        v = input("Would you like to enter verbose mode? (y/n): ")
        info.append(True if v == "y" else False)
        return info

    ## Configuration Menu ##
    def config(self):
        print("Configuration Menu")
        self.configOptions()

        while True:
            command = input("\nconfig > ").strip()

            match command:
                case "exit":
                    print("Returning to Home...")
                    break
                case "create":
                    self.addConfig()
                case "remove":
                    self.removeConfig()
                case "edit":
                    self.editConfig()
                case "list":
                    self.listConfig()
                case "help":
                    self.configOptions()
                case "display":
                    self.displayConfig()
                case _:
                    print("Unrecognized Command...")
                    
    ## Add configuration to configs.ini ##
    def addConfig(self):
        name = input("Enter configuration name: ")
        
        ## search for the entered name and notify the user if it already exists ##
        while self.configuration.has_section(name):
            print("Configuration name already exists.\nWould you like to 'edit' the existing config or 'create' a new one?")
            command = input("config > ")
            match command:
                case "edit":
                    self.editConfig()
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
        self.configuration.add_section(name)
        self.configuration[name]['turnIP'] = turnIP
        self.configuration[name]['turnPort'] = turnPort
        self.configuration[name]['encrypted'] = 1 if encrypt == "y" else 0

        self._saveConfig()
        
        print("Configuration successfully added!")
        
        # For when adding and immediately using
        return name
            

    ## Remove Configuration From configs.ini ##
    def removeConfig(self):
        self.listConfig()
        section = input("Choose section to remove: ")
        
        if self.configuration.has_section(section):
            self.configuration.remove_section(section)

            self._saveConfig()
            
            print("Configuration successfully removed!")
        else:
            print("Section does not exist...")

    ## Edit Configuration ##
    def editConfig(self):
        self.listConfig()
        section = input("Choose configuration to edit: ")
        
        if self.configuration.has_section(section):
            print("Sections:\n\tturnIP\n\tturnPort\n\tencrypted")
            
            while True:
                field = input("Choose field to edit: ")

                match field:
                    case "turnIP":
                        self.configuration[section]['turnIP'] = input("New turnIp: ")
                    case "turnPort":
                        self.configuration[section]['turnPort'] = input("New turnPort: ")
                    case "encrypted":
                        self.configuration[section]['encrypted'] = 1 if input("Encrypted? (y/n ): ") == "y" else 0
                    case _:
                        print("Invalid Field...")

                ## Write to configs.ini
                self._saveConfig()

                cont = input("Would you like to continue editing? (y/n)")
                if cont == "y":
                    continue
                elif cont == "n":
                    break
        
            print("Configuration successfully edited!")
        else:
            print("Section does not exist...")

    ## Display Configuration Fields ##  
    def displayConfig(self):
        self.listConfig()
        display = input("Choose configuration to display: ")
        if self.configuration.has_section(display):
            print("TURN IP: " + self.configuration[display]['turnIP'])
            print("TURN Port: " + self.configuration[display]['turnPort'])
            print("Encrypted: " + self.configuration[display]['encrypted'])
        else:
            print("Section does not exist...")
        
    ## Returns array containing all of the chosen configurations fields ##
    def getConfig(self, config):
        return [self.configuration[config]['turnIP'], self.configuration[config]['turnPort'], self.configuration[config]['encrypted']]    

    ## Lists the configuration names currently in config.ini ##
    def listConfig(self):
        print(self.configuration.sections())

    ## Options ##
    def configOptions(self):
        print("> create\n> remove\n> edit\n> list\n> display\n> help\n> exit\n")
        
    def getNumSections(self):
        return len(self.configuration.sections())

    def hasSection(self, config):
        return self.configuration.has_section(config)        
        
    def _saveConfig(self):
        with open(config_path, 'w') as configfile:
            self.configuration.write(configfile)
            
