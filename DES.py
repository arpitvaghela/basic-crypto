#!/usr/bin/env python3

from typing import List
import DES_tables as Table


def permutation(L: List[str], T: List[str]) -> List[str]:
    """returns permuted list based on table T:List[str]"""
    new_L = L.copy()
    for i in range(len(T)):
        new_L[i] = L[T[i] - 1]

    return new_L


def generate_bit(text: str) -> List[str]:
    """Convert characters to 8 bit utf-8,
        integers are converted to string
    """
    text = list(bytes(str(text), 'utf-8'))
    b_text = []
    for x in text:
        b = bin(x)[2:]
        if len(b) < 8:
            for _ in range(8 - len(b)):
                b = '0' + b
        byte = list(b)
        for bit in byte:
            b_text.append(bit)
    return b_text


def readFile(path: str) -> list:
    with open(path, 'rb') as file:
        b_file = list(file.read())
        b_text = []
        for x in b_file:
            b = bin(x)[2:]
            if len(b) < 8:
                for _ in range(8 - len(b)):
                    b = '0' + b
            byte = list(b)
            for bit in byte:
                b_text.append(bit)
        return b_text


def intTObin(i: int) -> List[str]:
    """ result of s_boxes are extended to 4 bits
    """
    s = bin(i)
    l = []
    s1 = ''
    if len(s[2:]) < 4:
        for _ in range(4 - len(s[2:])):
            s1 = s1 + '0'
    s1 = s1 + s[2:]
    for x in s1:
        l.append(x)
    return l


def bit_rotation(n: int, b_key: List[str]) -> List[str]:
    """breaks the list into 2 and rotate each by n:int times
    """
    left = b_key[:len(b_key) // 2].copy()
    right = b_key[(len(b_key) // 2):].copy()
    for _ in range(n):
        left.insert(0, left[-1])
        left.pop(-1)
        right.insert(0, right[-1])
        right.pop(-1)
    for x in right:
        left.append(x)
    return left


def subkey_generation(b_key: List[str]) -> List[List[str]]:
    """
        returns list of 16 subkeys of size 48
    """
    shift = [1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28]
    subkeys = []
    for i in range(16):
        subkeys.append(bit_rotation(shift[i], b_key))
        permutation(subkeys[i], Table.PC2)
        subkeys[i] = subkeys[i][:48]
    return subkeys


def key_generation(key: str) -> List[List[str]]:
    """ generate main key b_key and returns subkeys using subkey generator
    """
    b_key = generate_bit(key)
    while (len(b_key) < 64):
        print('short key, Enter new KEY:')
        b_key = generate_bit(input())
    #trim to 64 bits
    if (len(b_key) > 64):
        b_key = b_key[:64]
    #permute key
    b_key = permutation(b_key, Table.PC1)
    #key length to 56
    b_key = b_key[:56]
    subkey = subkey_generation(b_key)
    return subkey


def printList(list1: List[str]) -> None:
    """
        print the list of binary data as string
    """
    l = list1.copy()
    for i in range(len(l)):
        l[i] = str(l[i])
    print(''.join(l))


def strList(list1: List[str]) -> str:
    """
        return string of binary date
    """
    l = list1.copy()
    for i in range(len(l)):
        l[i] = str(l[i])
    return ''.join(l)


def binList(l: List[str]) -> int:
    """
    convert l:List[str] to int for usage S_box
    """
    for i in range(len(l)):
        l[i] = str(l[i])
    return int(''.join(l), 2)


def extend_right(right: list) -> list:
    """
    return expanded right permutation(right, Table.E)
    """
    for _ in range(16):
        right.append(0)
    return permutation(right, Table.E)


def s_box_replacement(right: List[str]) -> List[str]:
    r = []
    for x in range(8):
        r.append(right[x * 6:(x + 1) * 6])
    for x in range(len(r)):
        r[x] = Table.S_box[x][binList(r[x])]
        r[x] = intTObin(r[x])
    for x in r[1:]:
        for b in x:
            r[0].append(b)
    return r[0]


def strtobin_list(str1: list) -> List[int]:
    for i in range(len(str1)):
        str1[i] = int(str1[i])
    return str1


def fnc(right: list, subkey: list) -> List[int]:
    e_right = extend_right(right)
    r = []
    for i in range(len(e_right)):
        e_right[i] = int(e_right[i])

    for i in range(len(subkey)):
        subkey[i] = int(subkey[i])

    for i in range(len(subkey)):
        r.append(e_right[i] ^ subkey[i])
    r = s_box_replacement(r)
    r = permutation(r, Table.P)
    return r


def xor_list(L1: list, L2: list) -> list:
    l = []
    for i in range(len(L1)):
        l.append(L1[i] ^ L2[i])
    return l


def add_space(plaintext: str) -> str:
    """
    add spaces to plaintext if len(plaintext)%8 > 0
    """
    if len(plaintext) % 8 > 0:
        for _ in range(8 - len(plaintext) % 8):
            plaintext = plaintext + ' '
    return plaintext


def strTobytes(plaintext: str) -> list:
    plaintext = add_space(plaintext)
    plaintext = generate_bit(plaintext)
    return plaintext


def DES_encrypt(plaintext: str, key) -> list:
    subkeys = key_generation(key)
    plain_list = []
    for x in plaintext:
        plain_list.append(x)
    plaintext = plain_list
    blocks = []
    #create blocks
    for i in range(len(plaintext) // 64):
        blocks.append(plaintext[i * 64:(i + 1) * 64])
    encrypt_blocks = []
    for block in blocks:
        block = permutation(block, Table.IP)
        for i in range(16):
            left = block[:32].copy()
            right = block[32:].copy()
            block[:32] = right
            block[32:] = xor_list(strtobin_list(left),
                                  strtobin_list(fnc(right, subkeys[i])))
        block = permutation(block, Table.IP_inv)
        for x in block:
            encrypt_blocks.append(x)
    return encrypt_blocks


def DES_decrypt(crypt: list, key) -> list:
    subkeys = key_generation(key)
    blocks = []
    for i in range(len(crypt) // 64):
        block = []
        for x in range(64):
            block.append(crypt[i * 64 + x])
        blocks.append(block)
    plaintext = []
    for block in blocks:
        block = permutation(block, Table.IP)
        for i in range(16):
            left = block[:32].copy()
            right = block[32:].copy()
            block[32:] = left
            block[:32] = xor_list(strtobin_list(right),
                                  strtobin_list(fnc(left, subkeys[15 - i])))
        block = permutation(block, Table.IP_inv)
        for x in block:
            plaintext.append(x)
    return plaintext


def backTobytes(s: str) -> bytes:
    I_str = []
    for i in range(len(s) // 8):
        I_str.append(int(strList(s[i * 8:(i + 1) * 8]), 2))
    return bytes(I_str)


def DES3_encrypt(plaintext: str, key1, key2, key3) -> list:
    return DES_encrypt(DES_decrypt(DES_encrypt(plaintext, key1), key2), key3)


def DES3_decrypt(e_text: list, key1, key2, key3) -> list:
    return DES_decrypt(DES_encrypt(DES_decrypt(e_text, key3), key2), key1)


def DESX_xor(text: str, key) -> list:
    key = strtobin_list(generate_bit(key))[:64]
    b_text = []
    for x in text:
        b_text.append(int(x))

    final_text = []
    for i in range(len(b_text) // 64):
        x1 = xor_list(b_text[i * 64:(i + 1) * 64], key)
        for x in x1:
            final_text.append(x)
    return final_text


def DESX_encrypt(plaintext: str, key0, key1, key2) -> list:
    final_plaintext = DESX_xor(plaintext, key0)
    e_text = DES_encrypt(final_plaintext, key1)
    final_e_text = DESX_xor(e_text, key2)
    return final_e_text


def DESX_decrypt(e_text: list, key0, key1, key2) -> list:
    f_e_text = DESX_xor(e_text, key2)
    plaintest = DES_decrypt(f_e_text, key1)
    f_plaintext = DESX_xor(plaintest, key0)
    return f_plaintext


def DES_encrypt_file(path: str, key, outfilename: str = 'a.out') -> None:
    e = DES_encrypt(readFile(path), key)
    with open(outfilename, 'wb') as file:
        file.write(backTobytes(e))


def DES_decrypt_file(path: str, key, outfilename: str) -> None:
    p = DES_decrypt(readFile(path), key)
    with open(outfilename, 'wb') as file:
        file.write(backTobytes(p))


def DES3_encrypt_file(path: str, key1, key2, key3,
                      outfilename: str = 'a.out') -> None:
    e = DES3_encrypt(readFile(path), key1, key2, key3)
    with open(outfilename, 'wb') as file:
        file.write(backTobytes(e))


def DES3_decrypt_file(path: str, key1, key2, key3, outfilename: str) -> None:
    p = DES3_decrypt(readFile(path), key1, key2, key3)
    with open(outfilename, 'wb') as file:
        file.write(backTobytes(p))


def DESX_encrypt_file(path: str, key1, key2, key3,
                      outfilename: str = 'a.out') -> None:
    e = DESX_encrypt(readFile(path), key1, key2, key3)
    with open(outfilename, 'wb') as file:
        file.write(backTobytes(e))


def DESX_decrypt_file(path: str, key1, key2, key3, outfilename: str) -> None:
    p = DESX_decrypt(readFile(path), key1, key2, key3)
    with open(outfilename, 'wb') as file:
        file.write(backTobytes(p))


def bytesTomsg(msg: list) -> str:
    return str(backTobytes(msg))[2:-1]


#use strTobytes() before passing msg
#use bytesTomsg() to convert output to string

if __name__ == "__main__":
    e = DESX_encrypt(strTobytes('I\'m Feeling Lucky!'), '42234abc1', 22222222,
                     333333333)
    #print('e', e)
    p = DESX_decrypt(e, '42234abc1', 22222222, 333333333)
    #print('p', p)
    print(bytesTomsg(p))

    #x = DESX_encrypt('Hello, World!', 11111111, 22222222, 33333333)
    #DESX_decrypt(x, 11111111, 22222222, 33333333)
    #d1 = DES3_decrypt(e_text, 33333333, 22222222, 11111111)
    #print(e_text)
    #print(d1)
    #print(generate_bit('abc'), len(generate_bit('abc')))
    #DESX_encrypt_file('./download.jpeg', 11111111, 222222222, 3333333333)
    #DESX_decrypt_file('./a.out', 11111111, 222222222, 3333333333, 'out.jpeg')
