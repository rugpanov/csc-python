"""
Функция, выполняющая сравнение строк, содержащих русские буквы и
удовлетворяющая аксиоматике строгого порядка на всём множестве символов.
Функция обеспечивает лексикографический порядок строк
с учётом латинского и русского алфавитов: ASCII < АБВГДЕЁЖ...Я < абвгдеёж...я
"""
RUSSIAN_ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуф' \
                   'хцчшщъыьэюя'
SORTED_ALPHABET = {}
ANY_ALPHABET_CODE = -1
REPLACED_CHARS_NUMBER = 0


def __create_dict(alphabet):
    global SORTED_ALPHABET, ANY_ALPHABET_CODE, REPLACED_CHARS_NUMBER
    ANY_ALPHABET_CODE = ord(alphabet[0])
    current_code = ord(alphabet[0])
    for char in alphabet:
        SORTED_ALPHABET[char] = current_code
        if ord(char) != current_code:
            REPLACED_CHARS_NUMBER += 1
        current_code += 1


def use_russian_alphabet():
    """
    Настраивает глобальные параметры,
    используемые в alphabetic_key и alphabetic_less
    """
    __create_dict(RUSSIAN_ALPHABET)


def alphabetic_less(string1, string2):
    """
    Возвращает True, если string1 < string2
    """
    return alphabetic_key(string1) < alphabetic_key(string2)


def __char_to_key(char):
    index_in_alphabet = SORTED_ALPHABET.get(char)
    if index_in_alphabet is None:
        code = ord(char)
        if code > ANY_ALPHABET_CODE:
            return chr(code + REPLACED_CHARS_NUMBER)
        else:
            return char
    else:
        return chr(index_in_alphabet)


def alphabetic_key(string):
    """
    Возвращает некий ключ, такой, что
    (alphabetic_key(string1) < alphabetic_key(string2)) == \
    alphabetic_less(string1, string2)
    """
    builder = [__char_to_key(char) for char in string]
    return "".join(builder)