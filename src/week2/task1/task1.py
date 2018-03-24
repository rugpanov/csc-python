"""
Функция, выполняющая сравнение строк, содержащих русские буквы и
удовлетворяющая аксиоматике строгого порядка на всём множестве символов.
Функция обеспечивает лексикографический порядок строк
с учётом латинского и русского алфавитов: ASCII < АБВГДЕЁЖ...Я < абвгдеёж...я
"""
RUSSIAN_ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуф' \
                   'хцчшщъыьэюя'
LETTERS_TO_CHANGE_ORDER = "Ёё"

SORTED_ALPHABET = ""
ANY_ALPHABET_CODE = -1
REPLACED_CHARS_NUMBER = 0


def use_russian_alphabet():
    """
    Настраивает глобальные параметры,
    используемые в alphabetic_key и alphabetic_less
    """
    global SORTED_ALPHABET, ANY_ALPHABET_CODE, REPLACED_CHARS_NUMBER
    SORTED_ALPHABET = RUSSIAN_ALPHABET
    ANY_ALPHABET_CODE = ord(SORTED_ALPHABET[0])
    REPLACED_CHARS_NUMBER = len(LETTERS_TO_CHANGE_ORDER)


def alphabetic_less(string1, string2):
    """
    Возвращает True, если string1 < string2
    """
    return alphabetic_key(string1) < alphabetic_key(string2)


def alphabetic_key(string):
    """
    Возвращает некий ключ, такой, что
    (alphabetic_key(string1) < alphabetic_key(string2)) == \
    alphabetic_less(string1, string2)
    """

    builder = []
    for char in string:
        code = ord(char)
        index_in_alphabet = SORTED_ALPHABET.find(char)
        if index_in_alphabet == -1:
            if code > ANY_ALPHABET_CODE:
                builder.append(chr(code + REPLACED_CHARS_NUMBER))
            else:
                builder.append(char)
        else:
            builder.append(chr(ANY_ALPHABET_CODE + index_in_alphabet))
    return "".join(builder)
