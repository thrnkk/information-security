# Nomes: Luis Augusto Kuhn, Thomas Ricardo Reinke
from variables import s_box
from utils import string_to_hex_array, array_to_matrix, matrix_to_array, array_xor_array, galois_multiplication, array_split, printArray
from key_expansion import KeyExpansion
from base64 import b64encode


class AES(object):

    def __init__(self) -> None:
        pass

    def add_round_key(self, a: list, b: list) -> None:

        xor = array_xor_array(matrix_to_array(a), matrix_to_array(b))

        return array_split(xor, 4)

    def sub_bytes(self, a: list[list]) -> None:
        nova = []

        for i in matrix_to_array(a):
            nova.append(hex(s_box[int(i, 16)]))

        return array_split(nova, 4)

    def shift_rows(self, a) -> None:

        return [[a[0][0], a[0][1], a[0][2], a[0][3]],
                [a[1][1], a[1][2], a[1][3], a[1][0]],
                [a[2][2], a[2][3], a[2][0], a[2][1]],
                [a[3][3], a[3][0], a[3][1], a[3][2]], ]

    def mix_columns(self, a) -> None:

        cont = 0

        nova = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0], ]

        mult = [[2, 3, 1, 1],
                [1, 2, 3, 1],
                [1, 1, 2, 3],
                [3, 1, 1, 2], ]

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

    def pkcs5_pad(self, s):
        BLOCK_SIZE = 16

        return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

    def encryptFile(self, filePath: str, key: str, typeFile: str, outFile: str) -> None:

        s = ""

        if(typeFile == "text"):
            with open(filePath, "r") as f:

                s = self.encrypt(f.read(), key)

        elif (typeFile == "binary"):

            with open(filePath, "rb") as f:

                byte = b64encode(f.read())
                s = self.encrypt(str(byte), key)

        arquivo = open(outFile, "w")
        arquivo.write(printArray(s))

    def encrypt(self, text: str, key: str) -> None:

        F = []
        key_expansion = KeyExpansion()
        key_expansion.expand_key(key)
        textPad = self.pkcs5_pad(text)

        chunks, chunk_size = len(textPad), 16

        textList = [textPad[i:i+chunk_size]
                    for i in range(0, chunks, chunk_size)]

        for i in range(len(textList)):
            
            textPart = array_to_matrix(string_to_hex_array(textList[i]))

            A = self.add_round_key(
                textPart, key_expansion.get_current_round_key(0))

            for i in range(1, 10):

                B = self.sub_bytes(A)
                C = self.shift_rows(B)
                D = self.mix_columns(C)
                A = self.add_round_key(D, key_expansion.get_current_round_key(i))

            B = self.sub_bytes(A)
            C = self.shift_rows(B)
            E = self.add_round_key(C, key_expansion.get_current_round_key(10))
            F = F + array_to_matrix(matrix_to_array(E))

        return F


aes = AES()

key = '65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80'
# encrypted = aes.encrypt('DESENVOLVIMENTO!DESENVOLVIMENTO!', key)

encrypted = aes.encryptFile('assets\demo.txt', key, 'text', 'out5.txt')
print(encrypted)

