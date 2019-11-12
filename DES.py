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
        #code here
        b = bin(x)[2:]
        if len(b) < 8:
            for _ in range(8 - len(b)):
                b = '0' + b
        #print(len(b), b)
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
        #printList(subkeys[i])
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

    #print(b_key, len(b_key))
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
        #printList(r[x])
    for x in r[1:]:
        for b in x:
            r[0].append(b)
    #print(r[0], len(r[0]))
    return r[0]


def strtobin_list(str1: list) -> List[int]:
    for i in range(len(str1)):
        str1[i] = int(str1[i])
    return str1


def fnc(right: list, subkey: list) -> List[int]:
    #print('func:')

    e_right = extend_right(right)
    #printList(right)
    #print('e_right')
    #printList(e_right)
    r = []
    for i in range(len(e_right)):
        e_right[i] = int(e_right[i])

    for i in range(len(subkey)):
        subkey[i] = int(subkey[i])

    for i in range(len(subkey)):
        r.append(e_right[i] ^ subkey[i])
    #print('xor with subkey')
    #printList(r)
    r = s_box_replacement(r)
    #print('s_box')
    #printList(r)
    r = permutation(r, Table.P)
    #print('permute')
    #printList(r)
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


def DES_encrypt(plaintext, key):
    subkeys = key_generation(key)
    plaintext = add_space(plaintext)
    plaintext = generate_bit(plaintext)
    blocks = []
    #create blocks
    for i in range(len(plaintext) // 64):
        blocks.append(plaintext[i * 64:(i + 1) * 64])
    #printList(blocks)
    encrypt_blocks = ''
    for block in blocks:
        #print('Start:')
        #printList(block)
        block = permutation(block, Table.IP)
        #print('IP:')
        #printList(block)
        for i in range(16):
            left = block[:32].copy()
            right = block[32:].copy()
            block[:32] = right
            block[32:] = xor_list(strtobin_list(left),
                                  strtobin_list(fnc(right, subkeys[i])))
            #print('round', i)
            #printList(block)
        block = permutation(block, Table.IP_inv)
        #print('IP_inv:')
        #print(strList(block), len(block))
        encrypt_blocks = encrypt_blocks + strList(block)
    return encrypt_blocks


def DES_decrypt(crypt, key):
    subkeys = key_generation(key)
    blocks = []
    for i in range(len(crypt) // 64):
        block = []
        for x in range(64):
            block.append(crypt[i * 64 + x])
        blocks.append(block)
    plaintext = ''
    #print(blocks, len(blocks))
    for block in blocks:
        #print('D_Start:')
        #printList(block)
        block = permutation(block, Table.IP)
        #print('D-IP:')
        #printList(block)
        for i in range(16):
            left = block[:32].copy()
            right = block[32:].copy()
            block[32:] = left
            block[:32] = xor_list(strtobin_list(right),
                                  strtobin_list(fnc(left, subkeys[15 - i])))
            #print('D_round', 15 - i)
            #printList(block)
        block = permutation(block, Table.IP_inv)
        #print('D_IP_inv:')
        #print(strList(block), len(block))
        #print(type(block[0]))
        plaintext = plaintext + backToString(strList(block))
    return plaintext


def backToString(s: str) -> str:
    """
    convert block data back to string
    """
    I_str = []
    for i in range(len(s) // 8):
        I_str.append(int(s[i * 8:(i + 1) * 8], 2))
    return str(bytes(I_str), 'utf-8')


if __name__ == "__main__":
    print(
        DES_decrypt(DES_encrypt('I\'m Feeling Lucky!', 113234234543234),
                    113234234543234))
    #print(generate_bit('abc'), len(generate_bit('abc')))
