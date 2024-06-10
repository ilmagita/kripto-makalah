import hashlib

# keccak hash
def generate_keccak_hash(data, bit_length=256):
    if bit_length == 224:
        hash_obj = hashlib.sha3_224()
    elif bit_length == 256:
        hash_obj = hashlib.sha3_256()
    elif bit_length == 384:
        hash_obj = hashlib.sha3_384()
    elif bit_length == 512:
        hash_obj = hashlib.sha3_512()
    else:
        raise ValueError("Unsupported bit length for SHA-3")

    hash_obj.update(data)
    return hash_obj.hexdigest()