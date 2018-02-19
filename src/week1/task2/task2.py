smallNumberToStr = ["", "одна", "две", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять", "десять",
                    "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать",
                    "семнадцать", "восемнадцать", "девятнадцать"]

decadesToStr = ["-----",
                "десять",
                "двадцать",
                "тридцать",
                "сорок",
                "пятьдесят",
                "шестьдесят",
                "семьдесят",
                "восемьдесят",
                "девяносто"]

firstPartTemplate = "{bottles_number} бутыл{noun_end} стоял{verb_end} на столе,\n" \
                    "{bottles_number} бутыл{noun_end}!\n"

secondPartTemplate = "Одна из них упала,\n" \
                     "{bottles_number} бутыл{noun_end} остал{verb_end}сь на столе."

finalLines = "И вот она упала,\n" \
             "Ни одной бутылки не осталось на столе!"

noun_ends = {"singular": "ка",
             "paucal": "ки",
             "plural": "ок"}

verb_ends = {"singular": "а",
             "paucal": "и",
             "plural": "о"}


def number_to_str_with_title_letter(value):
    if value >= 20:
        decades = value // 10
        num = value % 10
        return (decadesToStr[decades].title() + " " + smallNumberToStr[num]).strip()
    else:
        return smallNumberToStr[value].title()


def is_plural(value):
    num = value % 10
    return num == 0 or num > 4 or 10 < value < 15


def is_paucal(value):
    num = value % 10
    return 1 < num < 5 and not (10 < value < 15)


def is_singular(value):
    num = value % 10
    return num == 1 and not (10 < value < 15)


def get_noun_end(value):
    if is_singular(value):
        return noun_ends["singular"]
    elif is_paucal(value):
        return noun_ends["paucal"]
    elif is_plural(value):
        return noun_ends["plural"]

    raise ValueError


def get_verb_end(value):
    if is_singular(value):
        return verb_ends["singular"]
    elif is_paucal(value):
        return verb_ends["paucal"]
    elif is_plural(value):
        return verb_ends["plural"]

    raise ValueError


def get_first_part_from_template(bottles_number):
    bottles_number_as_str = number_to_str_with_title_letter(bottles_number)
    noun_end = get_noun_end(bottles_number)
    verb_end = get_verb_end(bottles_number)
    return firstPartTemplate.format(bottles_number=bottles_number_as_str, noun_end=noun_end, verb_end=verb_end)


def get_second_part_from_template(bottles_number):
    bottles_number_as_str = number_to_str_with_title_letter(bottles_number)
    noun_end = get_noun_end(bottles_number)
    verb_end = get_verb_end(bottles_number)
    return secondPartTemplate.format(bottles_number=bottles_number_as_str, noun_end=noun_end, verb_end=verb_end)


def sing_song(bottles_number):
    result = ""
    for current_bottles_number in reversed(range(1, bottles_number + 1)):
        result += get_first_part_from_template(current_bottles_number)
        if current_bottles_number != 1:
            result += get_second_part_from_template(current_bottles_number - 1)
            result += "\n\n"
        else:
            result += finalLines
    return result.strip()


bottles_number_arg = int(input())
print(sing_song(bottles_number_arg))
