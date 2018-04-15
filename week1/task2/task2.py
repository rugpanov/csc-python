""" Стишек "99 бутылок"
Задание: Напишите программу, которая получает исходное количество бутылок (1...99)
и выводит текст песни, начиная с этого исходного количества:

Девяносто девять бутылок стояло на столе,
Девяносто девять бутылок!
Одна из них упала,
Девяносто восемь бутылок осталось на столе.

Девяносто восемь бутылок стояло на столе,
.....

Две бутылки стояли на столе,
Две бутылки!
Одна из них упала,
Одна бутылка осталась на столе.

Одна бутылка стояла на столе,
Одна бутылка!
И вот она упала,
Ни одной бутылки не осталось на столе
"""

NUMBER_TO_STR = ["", "одна", "две", "три", "четыре", "пять", "шесть", "семь",
                 "восемь", "девять", "десять", "одиннадцать", "двенадцать",
                 "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать",
                 "семнадцать", "восемнадцать", "девятнадцать"]

DECADE_TO_STR = ["-----",
                 "десять",
                 "двадцать",
                 "тридцать",
                 "сорок",
                 "пятьдесят",
                 "шестьдесят",
                 "семьдесят",
                 "восемьдесят",
                 "девяносто"]

FIRST_PART_TEMPLATE = """{bottles_number} бутыл{noun_end} стоял{verb_end} на столе,
{bottles_number} бутыл{noun_end}!\n"""

SECOND_PART_TEMPLATE = """Одна из них упала,
{bottles_number} бутыл{noun_end} остал{verb_end}сь на столе."""

FINAL_LINES = """И вот она упала,
Ни одной бутылки не осталось на столе!"""

NOUN_ENDS = {"singular": "ка",
             "paucal": "ки",
             "plural": "ок"}

VERB_ENDS = {"singular": "а",
             "paucal": "и",
             "plural": "о"}
SMALL_NUMBER_THRESHOLD = 20
DECADE_AS_NUMBER = 10
LINE_BREAKER = "\n\n"


def __number_to_str_with_title_letter(value):
    if value < SMALL_NUMBER_THRESHOLD:
        return NUMBER_TO_STR[value].title()

    decades = value // DECADE_AS_NUMBER
    num = value % DECADE_AS_NUMBER
    return (DECADE_TO_STR[decades].title() + " " + NUMBER_TO_STR[num]).strip()


def __is_plural(value):
    num = value % DECADE_AS_NUMBER
    return num == 0 or num > 4 or 10 < value < 15


def __is_paucal(value):
    num = value % DECADE_AS_NUMBER
    return 1 < num < 5 and not 10 < value < 15


def __is_singular(value):
    num = value % DECADE_AS_NUMBER
    return num == 1 and not 10 < value < 15


def __get_noun_end(value):
    if __is_singular(value):
        return NOUN_ENDS["singular"]
    elif __is_paucal(value):
        return NOUN_ENDS["paucal"]
    elif __is_plural(value):
        return NOUN_ENDS["plural"]

    raise ValueError


def __get_verb_end(value):
    if __is_singular(value):
        return VERB_ENDS["singular"]
    elif __is_paucal(value):
        return VERB_ENDS["paucal"]
    elif __is_plural(value):
        return VERB_ENDS["plural"]

    raise ValueError


def __get_first_part_from_template(bottles_number):
    bottles_number_as_str = __number_to_str_with_title_letter(bottles_number)
    noun_end = __get_noun_end(bottles_number)
    verb_end = __get_verb_end(bottles_number)
    return FIRST_PART_TEMPLATE.format(bottles_number=bottles_number_as_str,
                                      noun_end=noun_end, verb_end=verb_end)


def __get_second_part_from_template(bottles_number):
    bottles_number_as_str = __number_to_str_with_title_letter(bottles_number)
    noun_end = __get_noun_end(bottles_number)
    verb_end = __get_verb_end(bottles_number)
    return SECOND_PART_TEMPLATE.format(bottles_number=bottles_number_as_str,
                                       noun_end=noun_end, verb_end=verb_end)


def sing_song(bottles_number):
    """
    "Прочитать" стишек "99 бутылок"
    """

    result = ""
    for current_bottles_number in reversed(range(1, bottles_number + 1)):
        result += __get_first_part_from_template(current_bottles_number)
        if current_bottles_number != 1:
            result += __get_second_part_from_template(current_bottles_number - 1)
            result += LINE_BREAKER
        else:
            result += FINAL_LINES
    return result.strip()


print(sing_song(int(input())))
