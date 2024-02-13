class ZnajdowanieCiagu:
    def __init__(self, words):
        self.words = words

    def znajdz_najdluzszy_ciag_znakow(self):
        from itertools import permutations
        max_length = 0
        max_char = ''
        max_combination = ''

        for perm in permutations(self.words):
            long_word = ''.join(perm)
            current_max_length, max_char_in_perm = self._znajdz_najdluzszy_ciag_w_slowie(long_word)

            if current_max_length > max_length:
                max_length = current_max_length
                max_char = max_char_in_perm
                max_combination = long_word

        return max_length, max_char, max_combination

    def _znajdz_najdluzszy_ciag_w_slowie(self, word):
        max_length = 0
        current_length = 0
        max_char = ''
        prev_char = ''

        for char in word:
            if char == prev_char:
                current_length += 1
            else:
                if current_length > max_length:
                    max_length = current_length
                    max_char = prev_char
                current_length = 1
                prev_char = char
        if current_length > max_length:
            max_length = current_length
            max_char = prev_char

        return max_length, max_char

if __name__ == "__main__":
    debug = False

    if debug:
        words = ["mmm", "to", "wlasnie", "ja", "jestem", "mistrzem", "programowania"]
        ciag = ZnajdowanieCiagu(words)
        max_length, max_char, max_combination = ciag.znajdz_najdluzszy_ciag_znakow()
        print(f"Test r4c0: Najdłuższy ciąg to '{max_char}' powtarzający się {max_length} razy w kombinacji '{max_combination}', co jest najdłuższym ciągiem znaków.")
    else:
        n = int(input())
        words = []
        for _ in range(n):
            words.append(input())
        ciag = ZnajdowanieCiagu(words)
        max_length, max_char, max_combination = ciag.znajdz_najdluzszy_ciag_znakow()
        print(f"{max_length}")


