# Nomes: Luis Augusto Kuhn, Thomas Ricardo Reinke

from variables import s_box, l_table, e_table
from utils import bytes_string_to_hex_array, array_to_matrix, array_xor_array


class KeyExpansion(object):

    def __init__(self) -> None:
        self.key = []
        self.round_constant = (
            '0x01', '0x02', '0x04', '0x08', '0x10', '0x20', '0x40', '0x80', '0x1b', '0x36'
        )

    def get_last_round_key(self) -> list:

        round_key = [[], [], [], []]

        initial_pos = len(self.key[0]) - 4
        final_pos = len(self.key[0])

        round_key[0] = self.key[0][initial_pos : final_pos]
        round_key[1] = self.key[1][initial_pos : final_pos]
        round_key[2] = self.key[2][initial_pos : final_pos]
        round_key[3] = self.key[3][initial_pos : final_pos]

        return round_key

    def get_current_round_key(self, position: int) -> list:

        round_key = [[], [], [], []]

        initial_pos = position * 4
        final_pos = initial_pos + 4

        round_key[0] = self.key[0][initial_pos : final_pos]
        round_key[1] = self.key[1][initial_pos : final_pos]
        round_key[2] = self.key[2][initial_pos : final_pos]
        round_key[3] = self.key[3][initial_pos : final_pos]

        return round_key

    def get_word(self, position: int) -> list:

        round_key = self.get_last_round_key()

        return [i[position] for i in round_key]

    def rotate_bytes(self, a: list) -> list:

        return a[1:] + a[:1]

    def replace_word(self, word: list) -> list:

        return [hex(s_box[int(byte, 16)]) for byte in word]

    def get_round_constant(self, position: int) -> list:

        return [self.round_constant[position], '0x00', '0x00', '0x00']

    def key_add_word(self, word: list) -> None:

        self.key[0].append(word[0])
        self.key[1].append(word[1])
        self.key[2].append(word[2])
        self.key[3].append(word[3])

    def expand_key(self, key: list) -> list:

        self.key = array_to_matrix(bytes_string_to_hex_array(key))

        for i in range(10):

            last_word = self.get_word(3)
            rotated = self.rotate_bytes(last_word)
            replaced = self.replace_word(rotated)
            round_constant = self.get_round_constant(i)

            xored = array_xor_array(replaced, round_constant)

            word1 = array_xor_array(self.get_word(0), xored)
            word2 = array_xor_array(self.get_word(1), word1)
            word3 = array_xor_array(self.get_word(2), word2)
            word4 = array_xor_array(self.get_word(3), word3)

            self.key_add_word(word1)
            self.key_add_word(word2)
            self.key_add_word(word3)
            self.key_add_word(word4)

        return self.key