import sympy
import random
from math import gcd

## HELPER FUNCTIONS
def generate_large_prime():
    while True:
        number = random.randint(1, 9999999999)
        if sympy.isprime(number):
            return number
        
def next_prime(n):
    """Generate the next closest prime number if n is not a prime."""
    if n <= 1:
        return 2
    prime = n
    found = False
    
    if sympy.isprime(prime):
        found = True

    while not found:
        prime += 1
        if sympy.isprime(prime):
            found = True
    return prime

def reverse_number(number):
    reversed_str = str(number)[::-1]
    reversed_number = int(reversed_str)
    return reversed_number

## RSA FUNCTIONS
def generate_public_key(p, q, e):
    return (e, p * q)

def generate_private_key(p, q, e):
    totient = (p - 1) * (q - 1)
    d = sympy.mod_inverse(e, totient)
    return (d, p * q)

def is_relative_prime(a, b):
    return gcd(a, b) == 1

def generate_rsa_key(birthdate=27022003):
    birthdate = next_prime(birthdate)
    reversed_birthdate = next_prime(reverse_number(birthdate))
    p = birthdate
    q = reversed_birthdate

    while p == q:
        q = generate_large_prime()

    n = p * q
    totient = (p - 1) * (q - 1)
    
    e = generate_large_prime()
    while not is_relative_prime(e, totient):
        e = generate_large_prime()
    
    pubKey = generate_public_key(p, q, e)
    privKey = generate_private_key(p, q, e)

    return {
        "pubKey": {"e": pubKey[0], "n": pubKey[1]},
        "privKey": {"d": privKey[0], "n": privKey[1]}
    }

# ## EXAMPLE USAGE
# keys = generate_rsa_key(27022003)
# print(keys)

