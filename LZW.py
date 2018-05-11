# https://github.com/RadekSimkanic/Compression-and-transformation/blob/master/LZW/__init__.py
def compress(uncompressed, dict_size = 256):
    dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])

            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w: 
        result.append(dictionary[w])
    return result

# https://github.com/RadekSimkanic/Compression-and-transformation/blob/master/LZW/__init__.py
def decompress(compressed, dict_size = 256):
    from io import StringIO

    dictionary = {i: chr(i) for i in range(dict_size)}

    result = StringIO()
    w = compressed.pop(0)
    w = chr(w)
    result.write(w)

    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry

    return result.getvalue()

#import sys
#if __name__ == '__main__':
#    msg = 'This is a message.'
#    print(sys.getsizeof(msg))
#
#   com = compress(msg)
#    print(com)
#    print(sys.getsizeof(com))
#
#    dec = decompress(com)
#    print(dec)
#    print(sys.getsizeof(dec))