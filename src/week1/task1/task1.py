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

ANIMALS = ["курочка", "уточка", "индюшонок", "кисуня", "собачонка",
           "коровёнка", "поросёнок", "телевизор"]

ANIMALS_TO_BUY = {"курочка": "курочку",
                  "уточка": "уточку",
                  "индюшонок": "индюшонка",
                  "кисуня": "кисоньку",
                  "собачонка": "собачонку",
                  "коровёнка": "коровёнку",
                  "поросёнок": "поросёнка",
                  "телевизор": "телевизор"}

ANIMALS_TO_ACTION = {"курочка": "{animal} по зёрнышку кудах-тах-тах",
                     "уточка": "{animal} та-ти-та-та",
                     "индюшонок": "{animal} фалды-балды",
                     "кисуня": "А {animal} мяу-мяу",
                     "собачонка": "{animal} гав-гав",
                     "коровёнка": "{animal} муки-муки",
                     "поросёнок": "{animal} хрюки-хрюки",
                     "телевизор": "{animal} надо, надо, ведь у нас такое стадо"}

ASK_TO_BUY_TEMPLATE = "Бабушка, бабушка, купим {animal}!"
TIMES_TO_REPEAT = 2
LINE_BREAKER = "\n"


def __ask_to_buy(animal, times):
    result = ""
    line = ASK_TO_BUY_TEMPLATE.format(animal=ANIMALS_TO_BUY[animal])
    for _ in range(0, times):
        result += line + LINE_BREAKER
    return result


def __is_last_animal(animal_index):
    return animal_index == len(ANIMALS) - 1


def __ensure_capitalized(sub_string, target_string):
    return target_string if target_string.find(sub_string) \
        else target_string.replace(sub_string, sub_string.title())


def __tell_actions(animal_i):
    result = ""
    for i in reversed(range(0, animal_i + 1)):
        animal = ANIMALS[i]
        action = ANIMALS_TO_ACTION[animal].format(animal=animal)
        action = __ensure_capitalized(animal, action)
        result += action
        if __is_last_animal(animal_i):
            result += "!"
            break
        result += ("," + LINE_BREAKER) if i else ("." + LINE_BREAKER)
    return result


def sing_song():
    """
    "Пропеть" песенку "Курочка по зёрнышку"
    """

    result = ""
    for i, animal in enumerate(ANIMALS):
        animal = ANIMALS[i]
        result += __ask_to_buy(animal, TIMES_TO_REPEAT)
        result += __tell_actions(i)
        result += LINE_BREAKER
    return result.strip()


print(sing_song())
