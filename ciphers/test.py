import sympy

def next_prime(n):
    """Generate the next closest prime number if n is not a prime."""
    if n <= 1:
        return 2
    prime = n
    found =
    
    if sympy.isprime(prime):
        found = True

    while not found:
        prime += 1
        if sympy.isprime(prime):
            found = True
    return prime

print(next_prime(27022003))