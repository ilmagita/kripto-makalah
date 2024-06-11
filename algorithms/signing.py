import hashlib
import os

import os
import hashlib

def hash_file(file_path):
    # Calculate the hash of the file contents
    hash_obj = hashlib.sha3_256()
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(4096)  # Read in chunks to handle large files
            if not chunk:
                break
            hash_obj.update(chunk)
    return hash_obj.digest()

def sign_file(file_path, d, n):
    signature = pow(int.from_bytes(hash_file(file_path), byteorder='big'), d, n)
    base_name, file_extension = os.path.splitext(file_path)
    with open(base_name + '_signature.txt', 'w') as signature_file:
        signature_file.write(hex(signature))

def verify_signature(file_path, signature_path, e, n):
    file_hash = hash_file(file_path)
    with open(signature_path, 'r') as signature_file:
        signature = int(signature_file.read(), 16)
    decrypted_signature = pow(signature, e, n)
    return file_hash == decrypted_signature.to_bytes((decrypted_signature.bit_length() + 7) // 8, byteorder='big')


# Example usage


# RSA parameters
e = 4736592089
d = 795027992716457
n = 811256546672219

# Ensure the RSA keys satisfy the RSA relationship
print(f"e: {e}, d: {d}, n: {n}")

file_path = os.path.join(os.path.dirname(__file__), 'test.png')

with open(file_path, 'rb') as file:
    contents = file.read()

sign_file(file_path, d, n)
signature_path = os.path.join(os.path.dirname(__file__), 'test_signature.txt')
is_verified = verify_signature(file_path, signature_path, e, n)
print(f"Is signature verified: {is_verified}")