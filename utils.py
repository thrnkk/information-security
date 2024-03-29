# Nomes: Luis Augusto Kuhn, Thomas Ricardo Reinke

from variables import l_table, e_table

def bytes_string_to_hex_array(text: str) -> list:

    return [hex(int(i)) for i in text.split(',')]

def string_to_hex_array(text: str) -> list:
    
    return [hex(ord(text[i])) for i in range(len(text))]

def array_split(array: list, n: int) -> list:

    return [array[i:i + n] for i in range(0, len(array), n)]

def array_to_matrix(text: list) -> list:

    return [[text[i], text[i+4], text[i+8], text[i+12]] for i in range(4)]

def matrix_to_array(matrix: list) -> list:

    new_list = []
    for i in matrix:
        for j in i:
            new_list.append(j)
    return new_list

def array_xor_array(a: list, b: list) -> list:

    return [hex(int(i, 16) ^ int(j, 16)) for i, j in zip(a, b)]

def array_to_str(array: list) -> str:

    clean_string = ''
    for i in array:
        for n in i:
            clean_string += f' {n}'

    return clean_string

def galois_multiplication(a: int, b: int) -> int:

    value = 0

    if a == 0 or b == 0:
        return 0
    elif a == 1:
        return b
    elif b == 1:
        return a
    else:
        value = l_table[a] + l_table[b]

    return e_table[value % 255]