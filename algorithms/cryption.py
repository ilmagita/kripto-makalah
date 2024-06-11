from ciphers import rsa
import os
import base64

def write_keys_to_files(keys):
    pub_key = keys["pubKey"]
    priv_key = keys["privKey"]
    
    e = pub_key['e']
    n_pub = pub_key['n']
    
    d = priv_key['d']
    n_priv = priv_key['n']
    
    with open('./keys/key.pub', 'w') as pub_file:
        pub_file.write(f"({e}, {n_pub})")
    
    with open('./keys/key.pri', 'w') as priv_file:
        priv_file.write(f"({d}, {n_priv})")

def utf8_to_base64(utf8_text):
    return base64.b64encode(utf8_text.encode("utf-8")).decode("utf-8")

def base64_to_utf8(base64_text):
    utf8_text = base64.b64decode(base64_text).decode("utf-8")
    return utf8_text

def binary_data_to_int_array(binary_data):
    array_of_integers = [int(byte) for byte in binary_data]
    return array_of_integers

def int_array_to_binary_data(array_of_integers):
    binary_data = bytes(array_of_integers)
    return binary_data

## ENCRYPTION AND DECRYPTION

def encrypt_file(file_path, e, n):
    base_name, file_extension = os.path.splitext(file_path)

    with open(file_path, 'rb') as file:
        plainfile = file.read()
        plain_array = binary_data_to_int_array(plainfile)
        cipher = [hex(pow(num,e,n)) for num in plain_array]

        with open(base_name + '_encrypted' + file_extension, 'w') as encrypted_file:
            encrypted_bytes = ''
            for val in cipher:
                encrypted_bytes += str(val)

            encrypted_file.write(encrypted_bytes)

def decrypt_file(file_path, d, n):
    base_name, file_extension = os.path.splitext(file_path)

    with open(file_path, 'r') as file:
        cipherfile = file.read()
        cipherfile = cipherfile.split('0x')
        cipherfile = cipherfile[1:]

        cipher = (int('0x'+content,16) for content in cipherfile)
        plain = [(pow(num, d, n)) for num in cipher]
        plain = int_array_to_binary_data(plain)

        with open(base_name + '_decrypted' + file_extension, 'wb') as decrypted_file:
            decrypted_file.write(plain)