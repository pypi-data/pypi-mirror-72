class key:
    def key(keyres: str):
        key_List = {'000000': 'A', '000001': 'a', '000010': 'B', '000011': 'b', '000100': 'C', '000101': 'c', '000110': 'D', '000111': 'd', '001000': 'E', '001001': 'e', '001010': 'F', '001011': 'f', '001100': 'G', '001101': 'g', '001110': 'H', '001111': 'h', '010000': 'I', '010001': 'i', '010010': 'J', '010011': 'j', '010100': 'K', '010101': 'k', '010110': 'L', '010111': 'l', '011000': 'M', '011001': 'm', '011010': 'N', '011011': 'n', '011100': 'O', '011101': 'o', '011110': 'P', '011111': 'p', '100000': 'Q', '100001': 'q', '100010': 'R', '100011': 'r', '100100': 'S', '100101': 's', '100110': 'T', '100111': 't', '101000': 'U', '101001': 'u', '101010': 'V', '101011': 'v', '101100': 'W', '101101': 'w', '101110': 'X', '101111': 'x', '110000': 'Y', '110001': 'y', '110010': 'Z', '110011': 'z', '110100': ',', '110101': '.', '110110': '!', '110111': '?', '111000': ';', '111001': ':', '111010': '(', '111011': ')', '111100': '[', '111101': ']', '111110': '@', '111111': ' '}
        try:
            return key_List[keyres]
        except KeyError:
            return 'appear KeyError, please check the input.'

    def keys(keysres: str):
        global k
        key_list = []
        keyress = keysres.split(',')
        for k in range(0, len(keyress)):
            returnres = key.key(keyress[k])
            if returnres != 'appear KeyError, please check the input.':
                key_list.append(key.key(keyress[k]))
            else:
                return 'appear KeyError, please check the input.'
        return ''.join(key_list)


__version__ = '1.0.4'