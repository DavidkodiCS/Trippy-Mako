# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad

## RSA
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os
import configparser

# ## Saved Public Keys
# pub_keys = []
# ## Load Configuration File ##
# global configuration
# global config_path
# configuration = configparser.ConfigParser()

# # Get config directory from environment variable
# config_dir = os.getenv("CONFIG_DIR", "/peers")
# config_path = os.path.join(config_dir, "peers.ini")
# os.makedirs(config_dir, exist_ok=True)

# # Read existing configurations if the file exists
# if os.path.exists(config_path):
#     configuration.read(config_path)
    
# Encrypt Message
def encrypt_message(message):
    public_key = get_my_pub_key()
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

# Decrypt Message
def decrypt_message(ciphertext):
    private_key = get_my_priv_key()
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()

## Get Key
def get_my_pub_key():
    with open("keys/public_key.pem", "rb") as key_file:
        return serialization.load_pem_public_key(
            key_file.read(),     
        )
        
def get_my_priv_key():
    with open("keys/private_key.pem", "rb") as key_file:
        return serialization.load_pem_public_key(
            key_file.read(),     
        )
    
# def get_my_private_key():
#     file_path = "/keys/id_rsa"
    
#     try:
#         with open(file_path, "r") as key:
#             return key
#     except FileNotFoundError:
#         print("Error: File not found...")
#         return
    
# def get_peer_public_key():
#     print(configuration.sections)
#     peer = input("Please choose a peer from the list above: ")
    
#     if configuration.has_section(peer):
#         return configuration.get(peer)
#     else:
#         print("Invalid Selection")
#         return ""
    

## FOR NOW WE ARE ASSUMING THAT THE PEERS KNOW EACH OTHER'S KEYS
# ## Retrieve Peer Key
# def save_peer_key(pub_key):
#     name = input("Please enter a name for this peer: ")
    
#     configuration.add_section(name)
#     configuration[name]['pub_key'] = pub_key
    
#     with open(config_path, 'w') as configfile:
#         configuration.write(configfile)
    
#     print("Peer successfully added!")