import re

from .base.base import BasePhoneticsAlgorithm
from .config import RU_PHONEMES, FI_VOWELS, RU_VOWELS, EE_VOWELS, \
    RU_REPLACEMENT_VOWEL_MAP, RU_DEAF_CONSONANTS, EE_FI_DEAF_CONSONANTS, SE_VOWELS, SE_DEAF_CONSONANTS, \
    SE_PHONEMES


class Metaphone(BasePhoneticsAlgorithm):
    def __init__(self, compress_ending=False, reduce_word=True):
        """
        Initialization of Metaphone object
        :param compress_ending: not used
        :param reduce_word: remove repeated letters from word
        """
        self.__compress_ending = compress_ending
        self._reduce_word = reduce_word

    _deaf_consonants_seq = ''
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, '')
    _vowels_table = str.maketrans('', '')

    def _deaf_consonants_letters(self, word):
        return word

    def _reduce_deaf_consonants_letters(self, word, criteria):
        res = []
        for i, letter in enumerate(word):
            if letter in self._deaf_consonants_seq and (i == len(word) - 1 or word[i + 1].lower() not in criteria):
                letter = letter.translate(self._deaf_consonants)
            res += [letter]
        return ''.join(res)

    def _compress_ending(self, word):
        return word

    def _apply_metaphone_algorithm(self, word):
        if self._reduce_word:
            word = self._reduce_seq(word)
        word = word.translate(self._vowels_table)
        word = self._deaf_consonants_letters(word)
        if self.__compress_ending:
            word = self._compress_ending(word)
        return word.upper()

    def transform(self, word):
        return self._apply_metaphone_algorithm(word)


class RussianMetaphone(Metaphone):
    _vowels = RU_VOWELS
    _deaf_consonants_seq = RU_DEAF_CONSONANTS
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, 'пстфк')
    _vowels_table = str.maketrans(_vowels, 'ААААИИИИУУ')

    __j_vowel_regex = re.compile(r'[ий][ео]', re.I)

    _replacement_vowel_map = RU_REPLACEMENT_VOWEL_MAP
    _replacement_vowel_map.update({
        re.compile(r'[ъь]', re.I): ''
    })

    _replacement_phoneme_map = RU_PHONEMES

    def __init__(self, compress_ending=False, reduce_phonemes=False):
        super().__init__(compress_ending)
        self.reduce_phonemes = reduce_phonemes

    def _replace_j_vowels(self, word):
        for replace, result in self._replacement_vowel_map.items():
            word = replace.sub(result, word)
        return self.__j_vowel_regex.sub('и', word)

    def _reduce_phonemes(self, word):
        for replace, result in self._replacement_phoneme_map.items():
            word = replace.sub(result, word)
        return word

    def _compress_ending(self, word):
        return word

    def _deaf_consonants_letters(self, word):
        return self._reduce_deaf_consonants_letters(word, self._vowels + 'лмнр')

    def transform(self, word):
        if self.reduce_phonemes:
            word = self._reduce_phonemes(word)
        word = self._replace_j_vowels(word)
        return self._apply_metaphone_algorithm(word)


class FinnishMetaphone(Metaphone):
    _vowels = FI_VOWELS
    _deaf_consonants_seq = EE_FI_DEAF_CONSONANTS
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, 'pftk')
    _vowels_table = str.maketrans(FI_VOWELS, 'AAAIIIUU')

    __ng_replacement = re.compile(r'ng', re.I)
    __z_replacement = re.compile(r'z', re.I)
    __q_replacement = re.compile(r'q', re.I)
    __w_replacement = re.compile(r'w', re.I)
    __x_replacement = re.compile(r'x', re.I)

    def _deaf_consonants_letters(self, word):
        return self._reduce_deaf_consonants_letters(word, self._vowels + 'lmnr')

    def transform(self, word):
        word = self.__ng_replacement.sub('n', word)
        word = self.__z_replacement.sub('ts', word)
        word = self.__q_replacement.sub('kv', word)
        word = self.__w_replacement.sub('v', word)
        word = self.__x_replacement.sub('ks', word)
        return self._apply_metaphone_algorithm(word)


class EstonianMetaphone(Metaphone):
    _vowels = EE_VOWELS
    _deaf_consonants_seq = EE_FI_DEAF_CONSONANTS
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, 'pftk')
    _vowels_table = str.maketrans(EE_VOWELS, 'AAAIIIIUU')

    __cz_replacement = re.compile(r'[cz]', re.I)
    __q_replacement = re.compile(r'q', re.I)
    __w_replacement = re.compile(r'w', re.I)
    __x_replacement = re.compile(r'x', re.I)
    __y_replacement = re.compile(r'y', re.I)

    def _deaf_consonants_letters(self, word):
        return self._reduce_deaf_consonants_letters(word, self._vowels + 'lmnr')

    def transform(self, word):
        word = self.__cz_replacement.sub('ts', word)
        word = self.__q_replacement.sub('kv', word)
        word = self.__w_replacement.sub('v', word)
        word = self.__x_replacement.sub('ks', word)
        word = self.__y_replacement.sub('i', word)
        return self._apply_metaphone_algorithm(word)


class SwedenMetaphone(Metaphone):
    """
    Metaphone for Sweden language
    """
    _vowels = SE_VOWELS
    _deaf_consonants_seq = SE_DEAF_CONSONANTS
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, 'pftk')
    _vowels_table = str.maketrans(SE_VOWELS, 'AAIIIIIUU')

    _replacement_phoneme_map = SE_PHONEMES

    def _deaf_consonants_letters(self, word):
        return self._reduce_deaf_consonants_letters(word, self._vowels + 'lmnr')

    def transform(self, word):
        if word.endswith('on') and not word.endswith('hon'):
            word = word[:-2] + 'ån'
        for replace, result in self._replacement_phoneme_map.items():
            word = replace.sub(result, word)
        return self._apply_metaphone_algorithm(word)
