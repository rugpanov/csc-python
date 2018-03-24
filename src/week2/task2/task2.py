"""
    Выполнение форматирование файла на псевдо-латыни.
    Функция:
        - читает из input_file (например, из sys.stdin)
        - и выводит в output_file (например, в sys.stdout)
        - абзацы заявленной ширины desired_width,
        - выполняя переносы латинских слов по слогам, если use_hyphens = True,
        - расширяя пробелы, если expand_spaces = True
"""

import sys

VOWELS = "aeiouyYAEIOU"


def _read_file(input_file):
    file = open(input_file, encoding="utf8")
    contents = file.read()
    file.close()
    return contents


def _read(input_file):
    if isinstance(input, str):
        return _read_file(input_file)
    return "\n".join(input_file.readlines())


def _write_to_file(output_file, content):
    file = open(output_file, encoding="utf8", mode="w+")
    file.write(content)
    file.close()


def _write(output_file, content):
    if isinstance(output_file, str):
        _write_to_file(output_file, content)
    else:
        output_file.write(content)


def _is_vowel(letter):
    return VOWELS.find(letter) != -1


def _remove_single_first(parts):
    """
    Части массива передается по ссылке и тут же изменяется,
    т.ч. можно не возвращать значение. Создание клона слишком дорого и
    не обусловлено.
    """
    if len(parts) > 1 and len(parts[0]) == 1:
        parts[1] = parts[0] + parts[1]
        parts.pop(0)


def _remove_single_last(parts):
    """
    Части массива передается по ссылке и тут же изменяется,
    т.ч. можно не возвращать значение. Создание клона слишком дорого и
    не обусловлено.
    """
    if len(parts) > 1 and len(parts[len(parts) - 1]) == 1:
        parts[len(parts) - 2] += parts[len(parts) - 1]
        parts = parts[:-1]


def _separate_on_syllables(word):
    """
    Слово разбивается на слоги.
    Каждый слог содержит:
        - произвольное количество согласных в начале,
        - ровно одну гласную (будем считать, что все слоги открытые)
        - последний слог может содержать сколько угодно согласных в конце.
    Нельзя оставлять одну букву с любого края слова.
    Пунктуация не отрывается от слова. Знаков препинания внутри слова нет - только в конце.
    """
    parts = []
    builder = []
    for letter in word:
        if _is_vowel(letter):
            builder.append(letter)
            parts.append("".join(builder))
            builder.clear()
        else:
            builder.append(letter)

    if parts:
        parts[-1] += "".join(builder)
    else:
        parts.append("".join(builder))

    _remove_single_first(parts)
    _remove_single_last(parts)

    return parts


def _is_fit(word, cells_to_fill, desired_width):
    is_fit = len(word) + 1 <= cells_to_fill
    is_fit_as_only_word = len(word) == cells_to_fill == desired_width
    return is_fit or is_fit_as_only_word


def _split_on_two(word, cells_to_fill, desired_width):
    """
    Делит :param word на два так, чтобы первое можно было бы вписать в число :param cells_to_fill
    при заданной максимальной длинне строки :param desired_width.
    В случае, если деление не требуется, второе слово = None.
    В случае, если деление при заданных параметрах невозможно, первое слово = None.
    """
    if _is_fit(word, cells_to_fill, desired_width):
        return [word, None]

    parts = _separate_on_syllables(word)
    second_part_len = 0
    for i in range(len(parts) - 1, 0, -1):
        part = parts[i]
        second_part_len += len(part)

        is_only_word = cells_to_fill == desired_width
        required_symbols_number = 1 if is_only_word else 2
        if len(word) - second_part_len + required_symbols_number <= cells_to_fill:
            first_word = "".join(parts[:i]) + "-"
            next_lines_word = "".join(parts[i:])
            return [first_word, next_lines_word]

    return [None, word]


def _process_word(word, line_counter, words_for_line, builder, desired_width):
    [first, second] = _split_on_two(word, desired_width - line_counter, desired_width)
    is_end_of_line = line_counter != 0

    if second is None:
        words_for_line.append(first)
        if is_end_of_line:
            builder.append(" ".join(words_for_line))
            return [0, []]
        return [len(first), words_for_line]
    elif first is None:
        if is_end_of_line:
            builder.append(" ".join(words_for_line))
            return _process_word(second, 0, [], builder, desired_width)
        builder.append(second)
        return [0, []]
    else:
        words_for_line.append(first)
        builder.append(" ".join(words_for_line))
        return _process_word(second, 0, [], builder, desired_width)


def _execute_paragraph_hyphens(contents, desired_width):
    """
    Выполняет разбивку :param contents: на строки длинны
    :param desired_width: с переносами слов дефисами по слогам.
    Если слово очень длинное, то оно переносится несколько раз.
    Если слово очень длинное, но его невозможно перенести - оно выводится целиком.
    Будем считать, что дефисов и тире в исходном тексте нет.
    """
    all_words = contents.split()
    builder = []
    words_for_line = []
    char_counter = 0
    for word in all_words:
        required_symbols_number = 1 if words_for_line else 0
        if char_counter + len(word) + required_symbols_number <= desired_width:
            char_counter += len(word) + required_symbols_number
            words_for_line.append(word)
        else:
            [char_counter, words_for_line] = _process_word(word,
                                                           char_counter,
                                                           words_for_line,
                                                           builder,
                                                           desired_width)

    if words_for_line:
        builder.append(" ".join(words_for_line))

    return "\n".join(builder)


def _extend_spaces(line, required_spaces, extended_number):
    return line.replace(" " * required_spaces,
                        " " * (required_spaces + 1), extended_number)


def _expand_line_by_spaces(words, desired_width):
    if len(words) == 1:
        return words[0]

    char_counter = 0
    for word in words:
        char_counter += len(word)
    space_to_fill = desired_width - char_counter
    required_spaces = space_to_fill // (len(words) - 1)
    extended_spaces_number = space_to_fill - required_spaces * (len(words) - 1)
    line = (" " * required_spaces).join(words)
    return _extend_spaces(line, required_spaces, extended_spaces_number)


def _expand_paragraph_by_spaces(line, desired_width):
    """
    Разбивка пробелами последовательности :param words.
    Правила форматирования:
    - Ширина текста - :param desired_width: в строке.
    - Если два слова и пробел не влезли в ограничение по ширине, то только в
    этом случае оставляется одно слово в строке.
    - Серии пробельных символов должны быть одной ширины. Если при этом строка
    не достигает нужной нам ширины, то - для определённости - к первым пробелам
    добавляется по одному символу.
    - Не должно быть концевых пробелов.
    - Последняя строка абзаца может содержать одно слово и оказаться короче
    заданной ширины. Если там два слова и более - она расширяется.
    """

    all_line_words = line.split()
    builder = []
    words_for_line = []
    char_counter = 0
    for word in all_line_words:
        required_symbols_number = 1 if words_for_line else 0
        is_fit = char_counter + len(word) + required_symbols_number <= desired_width
        if not words_for_line or is_fit:
            char_counter += len(word) + required_symbols_number
            words_for_line.append(word)
        else:
            builder.append(_expand_line_by_spaces(words_for_line, desired_width))
            char_counter = len(word)
            words_for_line = [word]

    if words_for_line:
        builder.append(_expand_line_by_spaces(words_for_line, desired_width))

    return "\n".join(builder)


def pretty_print(desired_width, use_hyphens, expand_spaces,
                 input_file=sys.stdin, output_file=sys.stdout):
    """
    Выполнение форматирование файла на псевдо-латыни.

    :param desired_width: ширина абзацев
    :param use_hyphens: нужно ли выполнять переносы латинских слов по слогам
    :param expand_spaces: нужно ли расширять пробелы
    :param input_file: файл, из которого производиться чтение
    :param output_file: файл, в который производиться вывод
    """
    content = _read(input_file)

    if use_hyphens:
        builder = []
        lines = content.split("\n")
        for line in lines:
            if line:
                paragraph = _execute_paragraph_hyphens(line, desired_width)
                builder.append(paragraph)

        content = "\n".join(builder)

    if expand_spaces:
        builder = []
        lines = content.split("\n")
        for line in lines:
            if line:
                paragraph = _expand_paragraph_by_spaces(line, desired_width)
                builder.append(paragraph)

        content = "\n".join(builder)

    _write(output_file, content)
