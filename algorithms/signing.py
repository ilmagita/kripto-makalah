import os
import hashlib

def hash_binary_file(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()

    ascii_text = binary_data.decode('ascii', errors='ignore')

    hash_obj = hashlib.sha3_256()
    hash_obj.update(ascii_text.encode('utf-8'))
    hashed_result = hash_obj.digest()

    hashed_result_int_array = [byte for byte in hashed_result]
    return hashed_result_int_array

def sign_file(file_path, d, n):
    hashed_int_array = hash_binary_file(file_path)

    signature_array = []

    for ch in hashed_int_array:
        signature = pow(ch, d, n)
        signature_array.append(signature)

    base_name, _ = os.path.splitext(file_path)

    with open(base_name + '_signature.txt', 'w') as signature_file:
        signature_file.write(str(signature_array))

def verify_signature(file_path, signature_path, e, n):
    hashed_int_array = hash_binary_file(file_path)

    with open(signature_path, 'r') as signature_file:
        content = signature_file.read()
    
    content = content.replace('[', '').replace(']', '')
    signature_array = [int(byte) for byte in content.split(',')]

    decrypted_array = []

    for ch in signature_array:
        decrypted = pow(ch, e, n)
        decrypted_array.append(decrypted)

    return hashed_int_array == decrypted_array