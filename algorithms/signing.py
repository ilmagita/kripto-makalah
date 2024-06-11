from ciphers.sha import hash_message

def sign_message(plaintext, d, n):
    hashed_message = hash_message(plaintext)

    signature = pow(int(hashed_message, 16), d, n)
    return signature

def verify_signature(plaintext, signature, e, n):
    hashed_message = hash_message(plaintext)
    decrypted_signature = pow(signature, e, n)
    
    calculated_hash = int(hashed_message, 16)

    if decrypted_signature == calculated_hash:
        return True
    else:
        return False