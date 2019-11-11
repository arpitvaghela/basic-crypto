#!/usr/bin/env python3

from typing import List

stringutf = u'\u0020\u0021\u0022\u0023\u0024\u0025\
\u0026\u0027\u0028\u0029\u002a\u002b\u002c\u002d\u002e\
\u002f\u0030\u0031\u0032\u0033\u0034\u0035\u0036\u0037\
\u0038\u0039\u003a\u003b\u003c\u003d\u003e\u003f\u0040\
\u0041\u0042\u0043\u0044\u0045\u0046\u0047\u0048\u0049\
\u004a\u004b\u004c\u004d\u004e\u004f\u0050\u0051\u0052\
\u0053\u0054\u0055\u0056\u0057\u0058\u0059\u005a\u005b\
\u005c\u005d\u005e\u005f\u0060\u0061\u0062\u0063\u0064\
\u0065\u0066\u0067\u0068\u0069\u006a\u006b\u006c\u006d\
\u006e\u006f\u0070\u0071\u0072\u0073\u0074\u0075\u0076\
\u0077\u0078\u0079\u007a\u007b\u007c\u007d\u007e\u00a9\
\n\u00b0\u00d7\u00f7'


def inTable(val: str, table: List[str]) -> bool:
    for x in table:
        if x == val:
            return True
    return False


def extendTable(table: List[str]) -> None:

    for x in stringutf:
        if not inTable(x, table):
            table.append(x)


def removeDuplicate(table: List[str]) -> None:
    for x in table:
        for _ in range(table.count(x) - 1):
            table.pop(table.index(x, table.index(x) + 1))


def createTable(key: str) -> List[str]:
    table = []

    for x in key:
        table.append(x)

    removeDuplicate(table)

    extendTable(table)
    return table


def Check(x: str, y: str, table: List[str]) -> List[str]:
    index_x = table.index(x)
    index_y = table.index(y)

    # row check
    if index_x // 10 == index_y // 10:
        x = table[10 * (index_x // 10) + (index_x + 1) % 10]
        y = table[10 * (index_y // 10) + (index_y + 1) % 10]

    #column check
    elif index_x % 10 == index_y % 10:
        x = table[(index_x + 10) % 100]
        y = table[(index_y + 10) % 100]

    # else
    else:
        x = table[10 * (index_x // 10) + (index_y) % 10]
        y = table[10 * (index_y // 10) + (index_x) % 10]

    return [x, y]


def encrypt_playfiar(text: str, key: str) -> str:
    table = createTable(key)
    text = list(text)

    if len(text) % 2 == 1:
        text.append('.')
    #print(text)

    for i in range(len(text) // 2):

        x = text[2 * i]
        y = text[2 * i + 1]
        a = Check(x, y, table)
        text[2 * i] = a[0]
        text[2 * i + 1] = a[1]
    string_text = ''.join(text)
    #print(string_text)
    return string_text


def inv(x: str, y: str, table: List[str]) -> List[str]:
    index_x = table.index(x)
    index_y = table.index(y)

    # row inverse
    if index_x // 10 == index_y // 10:
        x = table[10 * (index_x // 10) + (index_x - 1) % 10]
        y = table[10 * (index_y // 10) + (index_y - 1) % 10]

    #column inverse
    elif index_x % 10 == index_y % 10:
        x = table[(index_x - 10) % 100]
        y = table[(index_y - 10) % 100]

    # else square inverse
    else:
        x = table[10 * (index_x // 10) + (index_y) % 10]
        y = table[10 * (index_y // 10) + (index_x) % 10]

    return [x, y]


def decrypt_playfair(text: str, key: str) -> str:
    table = createTable(key)
    text = list(text)
    #print(text)

    for i in range(len(text) // 2):
        x = text[2 * i]
        y = text[2 * i + 1]
        a = inv(x, y, table)
        text[2 * i] = a[0]
        text[2 * i + 1] = a[1]

    if (text[-1] == '.'):
        text = text[:-1]
    string_text = ''.join(text)

    #print(string_text)
    return string_text


if __name__ == "__main__":
    key = u"\nHello$#World"
    text = "$arpit 123"
    enc_text = encrypt_playfiar(text, key)
    print(encrypt_playfiar(text, key))
    print(decrypt_playfair(enc_text, key))
