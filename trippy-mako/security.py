from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os
import configparser

## Load Configuration File ##
global configuration
global config_path
configuration = configparser.ConfigParser()

# Get config directory from environment variable
config_dir = os.getenv("CONFIG_DIR", "/")
config_path = os.path.join(config_dir, "peers.ini")
os.makedirs(config_dir, exist_ok=True)

# Read existing configurations if the file exists
if os.path.exists(config_path):
    configuration.read(config_path)
    
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
    