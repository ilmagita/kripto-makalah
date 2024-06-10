from ciphers import rsa

def encrypt(plaintext, pub_key):
    e = pub_key['e']
    n = pub_key['n']
    cipher_array = [pow(ord(char), e, n) for char in plaintext]

    hex_code = f''

    for c in cipher_array:
        hex_code = hex_code + hex(c)

    return hex_code

def decrypt(ciphertext, priv_key):
    d = priv_key['d']
    n = priv_key['n']
    plaintext_array = []

    ciphertext = ciphertext.strip()
    if ciphertext.startswith('0x'):
        parts = ciphertext.split('0x')[1:]
        for part in parts:
            plaintext_array.append(int(part, 16))
    
    plaintext = ''
    for char in plaintext_array:
        plaintext = plaintext + (chr(pow(char, d, n)))
    
    return plaintext

rsa_key = rsa.generate_rsa_key()
print(rsa_key)

pub_key = rsa_key['pubKey']
priv_key = rsa_key['privKey']

msg = encrypt(' h3ll0!! apa kabar ?!@', pub_key)
decrypt_msg = decrypt(msg, priv_key)
print(msg)
print(decrypt_msg)
