class lock:
    def lock(lockres: str):
        lock_List = {'A': '000000', 'a': '000001', 'B': '000010', 'b': '000011', 'C': '000100', 'c': '000101', 'D': '000110', 'd': '000111', 'E': '001000', 'e': '001001', 'F': '001010', 'f': '001011', 'G': '001100', 'g': '001101', 'H': '001110', 'h': '001111', 'I': '010000', 'i': '010001', 'J': '010010', 'j': '010011', 'K': '010100', 'k': '010101', 'L': '010110', 'l': '010111', 'M': '011000', 'm': '011001', 'N': '011010', 'n': '011011', 'O': '011100', 'o': '011101', 'P': '011110', 'p': '011111', 'Q': '100000', 'q': '100001', 'R': '100010', 'r': '100011', 'S': '100100', 's': '100101', 'T': '100110', 't': '100111', 'U': '101000', 'u': '101001', 'V': '101010', 'v': '101011', 'W': '101100', 'w': '101101', 'X': '101110', 'x': '101111', 'Y': '110000', 'y': '110001', 'Z': '110010', 'z': '110011', ',': '110100', '.': '110101', '!': '110110', '?': '110111', ';': '111000', ':': '111001', '(': '111010', ')': '111011', '[': '111100', ']': '111101', '@': '111110', ' ': '111111'}
        try:
            return lock_List[lockres]
        except KeyError:
            return 'appear KeyError,please check the input.'

    def locks(locksres: str):
        global l
        lock_list = []
        for l in range(0, len(str(locksres))):
            returnres = lock.lock(str(locksres)[l])
            if returnres != 'appear KeyError,please check the input.':
                lock_list.insert(l, returnres)
            else:
                return 'appear KeyError,please check the input.'
        return ','.join(lock_list)


__version__ = '1.0.4'