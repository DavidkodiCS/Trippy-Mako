# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
    
def encrypt_message(key, plaintext):
    iv = os.urandom(12)  # AES-GCM requires a 12-byte IV
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv + ciphertext  # Include IV for decryption

def decrypt_message(key, encrypted_data):
    iv = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# ## Encrypt / Decrypt
# def encrypt_cbc(in_plain_file, out_cipher_file, key, iv):
#     plain = ""
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     with open(in_plain_file, "rb") as f:
#         plain = bytes(f.read())

#     plain = pad(plain, 16)
#     ciphertext = cipher.encrypt(plain)

#     with open(out_cipher_file, "wb") as f:
#         f.write(ciphertext)

# def decrypt_cbc(in_cipher_file, out_plain_file, key, iv):
#     cipherT = ""
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     with open(in_cipher_file, "rb") as f:
#         cipherT = bytes(f.read())

#     plaintext = cipher.decrypt(cipherT)
#     plaintext = unpad(plaintext, 16)

#     with open(out_plain_file, "wb") as f:
#         f.write(plaintext)

# def encrypt_ctr(in_plain_file, out_cipher_file, key, ctr):
#     plain = ""

#     cipher = AES.new(key, AES.MODE_CTR, initial_value=ctr[-8:], nonce=ctr[:8])
#     with open(in_plain_file, "rb") as f:
#         plain = bytes(f.read())

#     ciphertext = cipher.encrypt(plain)

#     with open(out_cipher_file, "wb") as f:
#         f.write(ciphertext)

# def decrypt_ctr(in_cipher, out_plain, key, ctr):
#     cipherT = ""

#     cipher = AES.new(key, AES.MODE_CTR, initial_value=ctr[-8:], nonce=ctr[:8])
#     with open(in_cipher, "rb") as f:
#         cipherT = bytes(f.read())

#     plaintext = cipher.decrypt(cipherT)

#     with open(out_plain, "wb") as f:
#         f.write(plaintext)

# ## PART 3 ##
# def pad2(data):
#     l = len(data)
#     pad = 0
    
#     if(l < 16):
#         pad = 16 - l
#     elif(l > 16):
#         while (pad + l) % 16 != 0:
#             pad += 1
#     else:
#         pad = 16
    
#     for _ in range(pad):
#         data += bytes.fromhex(f"{pad:02x}")
        
#     return data
    
# def unpad2(data):
#     if (len(data) % 16) != 0:
#         print("padding error!")
#         return
    
#     paddingLen = data[-1]
#     padding = data[-paddingLen:]
    
#     if len(set(padding)) != 1:
#         print("padding error!")
#         return
        
#     return data[:-paddingLen]
