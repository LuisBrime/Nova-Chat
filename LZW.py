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
    dictionary = {i: chr(i) for i in range(dict_size)}

    result = []
    w = compressed.pop(0)
    w = chr(w)
    result.append(w)

    for k in compressed:
        if k < dict_size:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.append(entry)

        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry

    clear_result = []
    for item in result:
        if len(item) == 1:
            clear_result.append(item)
            continue
        for char in item:
            clear_result.append(char)

    return clear_result
