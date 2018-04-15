"""Песенка "Курочка по зёрнышку" (Im Radio ist ein Kucken)
Текст песенки:

Бабушка, бабушка, купим курочку!
Бабушка, бабушка, купим курочку!
Курочка по зёрнышку кудах-тах-тах.

Бабушка, бабушка, купим уточку! (2 раза)
Уточка та-ти-та-та,
Курочка по зёрнышку кудах-тах-тах.

Далее персонажи такие:

...индюшонка - Индюшонок фалды-балды,
...кисоньку - А кисуня мяу-мяу,
...собачонку - Собачонка гав-гав,
...коровёнку - Коровёнка муки-муки,
...поросёнка - Поросёнок хрюки-хрюки,
и заканчивается всё последним куплетом:

Бабушка, бабушка, купим телевизор! (2 раза)
Телевизор надо, надо, ведь у нас такое стадо!

﻿Примечание. "(2 раза)" - это два раза повторить одну строку.
"""

FIRST_FORM = 0
TO_BUY_FORM = 1
PHRASE_TEMPLATE = 2
ANIMALS = [["курочка", "курочку", "{animal} по зёрнышку кудах-тах-тах"],
           ["уточка", "уточку", "{animal} та-ти-та-та"],
           ["индюшонок", "индюшонка", "{animal} фалды-балды"],
           ["кисуня", "кисоньку", "А {animal} мяу-мяу"],
           ["собачонка", "собачонку", "{animal} гав-гав"],
           ["коровёнка", "коровёнку", "{animal} муки-муки"],
           ["поросёнок", "поросёнка", "{animal} хрюки-хрюки"],
           ["телевизор", "телевизор", "{animal} надо, надо, ведь у нас такое стадо"]]

ASK_TO_BUY_TEMPLATE = "Бабушка, бабушка, купим {animal}!"
TIMES_TO_REPEAT = 2
LINE_BREAKER = "\n"


def __ask_to_buy(animal_i, times):
    result = ""
    line = ASK_TO_BUY_TEMPLATE.format(animal=ANIMALS[animal_i][TO_BUY_FORM])
    for _ in range(0, times):
        result += line + LINE_BREAKER
    return result


def __is_last_index(index):
    return index == len(ANIMALS) - 1


def __ensure_capitalized(sub_string, target_string):
    return target_string if target_string.find(sub_string) \
        else target_string.replace(sub_string, sub_string.title())


def __tell_actions(current_animal_i):
    result = ""
    for i in reversed(range(0, current_animal_i + 1)):
        action = ANIMALS[i][PHRASE_TEMPLATE].format(animal=ANIMALS[i][FIRST_FORM])
        action = __ensure_capitalized(ANIMALS[i][FIRST_FORM], action)
        result += action
        if __is_last_index(i):
            result += "!"
            break
        result += ("," + LINE_BREAKER) if i else ("." + LINE_BREAKER)
    return result


def sing_song():
    """
    "Пропеть" песенку "Курочка по зёрнышку"
    """

    result = ""
    for i in range(0, len(ANIMALS)):
        result += __ask_to_buy(i, TIMES_TO_REPEAT)
        result += __tell_actions(i)
        result += LINE_BREAKER
    return result.strip()


print(sing_song())
