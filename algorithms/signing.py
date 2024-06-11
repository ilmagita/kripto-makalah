import hashlib
import os

def sign_message(plaintext, d, n):
    hash_obj = hashlib.sha3_256()
    hash_obj.update(plaintext)
    hashed_message = hash_obj.hexdigest()
    print(f"Hashed message (sign): {hashed_message}")

    signature = pow(int(hashed_message, 16), d, n)
    print(f"Signature: {signature}")
    return signature

def verify_signature(plaintext, signature, e, n):
    hash_obj = hashlib.sha3_256()
    hash_obj.update(plaintext)
    hashed_message = hash_obj.hexdigest()
    print(f"Hashed message (verify): {hashed_message}")

    decrypted_signature = pow(signature, e, n)
    print(f"Decrypted signature: {decrypted_signature}")
    calculated_hash = int(hashed_message, 16)
    
    return decrypted_signature == calculated_hash

# RSA parameters
e = 4736592089
d = 795027992716457
n = 811256546672219

# Ensure the RSA keys satisfy the RSA relationship
print(f"e: {e}, d: {d}, n: {n}")

file_path = os.path.join(os.path.dirname(__file__), 'test.png')

with open(file_path, 'rb') as file:
    contents = file.read()

signed = sign_message(contents, d, n)
is_verified = verify_signature(contents, signed, e, n)
print(f"Is signature verified: {is_verified}")