from random import randrange
from math import gcd, log
from collections import namedtuple
from binascii import hexlify, unhexlify

def is_prime(n, k=30):
    if n <= 3:
        return n == 2 or n == 3
    nega = n - 1

    sas, dad = 0, nega
    while not dad & 1:
        sas, dad = sas + 1, dad >> 1
    assert 2 ** sas * dad == nega and dad & 1

    for x in range(k):
        aaa = randrange(2, nega)
        i = pow(aaa, dad, n)
        if i in (1, nega):
            continue
        for r in range(1, sas):
            i = i ** 2 % n
            if i == 1:
                return False
            if i == nega:
                break
        else:
            return False
    return True

def randprime(N=10 ** 8):
    p = 1
    while not is_prime(p):
        p = randrange(N)
    return p

def multinv(modulus, value):
    x, lastx = 0, 1
    a, b = modulus, value
    while b:
        a, q, b = b, a // b, a % b
        x, lastx = lastx - q * x, x
    result = (1 - lastx * modulus) // value
    if result < 0:
        result += modulus
    assert 0 <= result < modulus and value * result % modulus == 1
    return result

KeyPair = namedtuple('KeyPair', 'public private')
Key = namedtuple('Key', 'exponent modulus')

def keygen(N, public=None):
    prime1 = randprime(N)
    prime2 = randprime(N)
    composite = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)

    if public is None:
        while True:
            private = randrange(totient)
            if gcd(private, totient) == 1:
                break
        public = multinv(totient, private)
    else:
        private = multinv(totient, public)
    assert public * private % totient == gcd(public, totient) == gcd(private, totient) == 1
    assert pow(pow(1234567, public, composite), private, composite) == 1234567
    return KeyPair(Key(public, composite), Key(private, composite))

def decypher(bcipher, prk, puk, verbose=False):
    chunksize = int(log(puk.modulus, 256))
    outchunk = chunksize + 1
    outfmt = '%%0%dx' % (chunksize * 2,)
    result = []
    for start in range(0, len(bcipher), outchunk):
        bcoded = bcipher[start: start+outchunk]
        coded = int(hexlify(bcoded),16)
        plain = pow(coded, *prk)
        chunk = unhexlify((outfmt % plain).encode())
        result.append(chunk)
    return b''.join(result).rstrip(b'\x00').decode()

def cypher(msg, puk, verbose=False):
    chunksize = int(log(puk.modulus, 256))
    outchunk = chunksize + 1
    outfmt = '%%0%dx' % (outchunk * 2,)
    bmsg = msg.encode()
    result = []
    for start in range(0, len(bmsg), chunksize):
        chunk = bmsg[start:start+chunksize]
        chunk += b'\x00' * (chunksize - len(chunk))
        plain = int(hexlify(chunk), 16)
        coded = pow(plain, *puk)
        bcoded = unhexlify((outfmt % coded).encode())
        result.append(bcoded)
    return b''.join(result)

def nsa(msg):
    nm = msg[::-1]
    nm = nm[len(nm)//2:len(nm)-1] + nm[0:len(nm)//2-1]
    nm = nm[::-1]
    nm += 'JN821741!3'
    nm = nm[len(nm) // 2:len(nm) - 1] + nm[0:len(nm) // 2 - 1]
    nm = nm[::-1]
    nm = nm[len(nm) // 2:len(nm) - 1] + nm[0:len(nm) // 2 - 1]
    return nm