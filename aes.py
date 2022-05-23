# Nomes: Luis Augusto Kuhn, Thomas Ricardo Reinke

from variables import s_box
from utils import string_to_hex_array, array_to_matrix, matrix_to_array, array_xor_array, galois_multiplication, array_split, array_to_str
from key_expansion import KeyExpansion
from base64 import b64encode
import mimetypes

class AES(object):

    def __init__(self) -> None:
        pass

    def add_round_key(self, a: list, b: list) -> list:

        xor = array_xor_array(matrix_to_array(a), matrix_to_array(b))

        return array_split(xor, 4)

    def sub_bytes(self, a: list[list]) -> list:
        nova = []

        for i in matrix_to_array(a):
            nova.append(hex(s_box[int(i, 16)]))

        return array_split(nova, 4)

    def shift_rows(self, a: list) -> list:

        return [[a[0][0], a[0][1], a[0][2], a[0][3]],
                [a[1][1], a[1][2], a[1][3], a[1][0]],
                [a[2][2], a[2][3], a[2][0], a[2][1]],
                [a[3][3], a[3][0], a[3][1], a[3][2]],]

    def mix_columns(self, a: list) -> list:

        cont = 0

        nova = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],]

        mult = [[2, 3, 1, 1],
                [1, 2, 3, 1],
                [1, 1, 2, 3],
                [3, 1, 1, 2],]

        for col in range(4):
            for row in range(4):

                r1 = galois_multiplication(
                    int(a[0][cont // 4], 16), mult[cont % 4][0])
                
                r2 = galois_multiplication(
                    int(a[1][cont // 4], 16), mult[cont % 4][1])
                
                r3 = galois_multiplication(
                    int(a[2][cont // 4], 16), mult[cont % 4][2])
                
                r4 = galois_multiplication(
                    int(a[3][cont // 4], 16), mult[cont % 4][3])

                b = (r1 ^ r2 ^ r3 ^ r4)

                nova[row][col] = hex(b)

                cont += 1

        return nova

    def pkcs5_padding(self, s: str) -> str:
        block_size = 16

        return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)

    def encrypt_file(self, file_path: str, key: str, output_file: str) -> None:

        s = ""
        if mimetypes.guess_type(file_path)[0] == 'text/plain':
            with open(file_path, "r") as f:
                s = self.encrypt(f.read(), key)
        else:
            with open(file_path, "rb") as f:
                s = self.encrypt(str(f.read()), key)

        file = open(output_file, "w")
        file.write(array_to_str(s))

    def encrypt(self, text: str, key: str) -> list:

        F = []
        
        key_expansion = KeyExpansion()
        key_expansion.expand_key(key)
        
        text_padded = self.pkcs5_padding(text)

        chunks, chunk_size = len(text_padded), 16

        text_chunks = [text_padded[i : i + chunk_size] for i in range(0, chunks, chunk_size)]

        for i in text_chunks:
            
            text = array_to_matrix(string_to_hex_array(i))

            A = self.add_round_key(text, key_expansion.get_current_round_key(0))

            for i in range(1, 10):

                B = self.sub_bytes(A)
                C = self.shift_rows(B)
                D = self.mix_columns(C)
                A = self.add_round_key(D, key_expansion.get_current_round_key(i))

            B = self.sub_bytes(A)
            C = self.shift_rows(B)
            E = self.add_round_key(C, key_expansion.get_current_round_key(10))
            
            F += array_to_matrix(matrix_to_array(E))

        return F


aes = AES()
key1 = '65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80'

aes.encrypt_file('assets\\demo.txt', key1, 'out0.txt')
aes.encrypt_file('assets\\sample.bin', key1, 'out1.txt')
aes.encrypt_file('assets\\arquivo1.jpg', key1, 'out2.txt')

key2 = '10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160'
aes.encrypt_file('assets\\arquivo-b.gif', key2, 'out3.txt')
