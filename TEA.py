from binascii import hexlify, unhexlify
import operator
import sys


def main():
    v = [0, 0]  # to be enciphered, 64 bits
    k = [0, 0, 0, 0]  # key to use, 128 bits

    # convert ascii to long integer
    v[0] = mkbits("The ")
    v[1] = mkbits("rain")

    k[0] = mkbits("This")
    k[1] = mkbits(" is ")
    k[2] = mkbits("pass")
    k[3] = mkbits("word")

    print("Plaintext: " + mkwords(v[0]) + mkwords(v[1]))

    print(v)

    c = encipher(v, k)
    print(c)

    d = decipher(c, k)
    print(d)

    print("Deciphered: " + mkwords(d[0]) + mkwords(d[1]))


# a couple utility functions
def mkbits(thestr):
    return int(eval('0x' + hexlify(thestr)),2)


def mkwords(thebits):
    return unhexlify(hex(thebits)[2:-1])


# see http://vader.brad.ac.uk/tea/tea.shtml
def encipher(v, k):
    y = v[0]
    z = v[1]
    sum = 0
    delta = 0x9E3779B9
    n = 32
    w = [0, 0]
    while (n > 0):
        y += (z << 4 ^ z >> 5) + z ^ sum + k[sum & 3]
        operator.iand(y, sys.maxsize) # maxsize of 32-bit integer
        sum += delta
        z += (y << 4 ^ y >> 5) + y ^ sum + k[sum >> 11 & 3]
        operator.iand(z, sys.maxsize)
        n -= 1

    w[0] = y
    w[1] = z
    return w


def decipher(v, k):
    y = v[0]
    z = v[1]
    sum = 0xC6EF3720
    delta = 0x9E3779B9
    n = 32
    w = [0, 0]
    # sum = delta<<5, in general sum = delta * n

    while (n > 0):
        z -= (y << 4 ^ y >> 5) + y ^ sum + k[sum >> 11 & 3]
        operator.iand(z, sys.maxsize)
        sum -= delta
        y -= (z << 4 ^ z >> 5) + z ^ sum + k[sum & 3]
        operator.iand(y, sys.maxsize)
        n -= 1

    w[0] = y
    w[1] = z
    return w

if __name__ == "__main__":
    main()