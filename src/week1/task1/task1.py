animals = ["курочка", "уточка", "индюшонок", "кисуня", "собачонка", "коровёнка", "поросёнок", "телевизор"]

animalToBuy = {"курочка": "курочку",
               "уточка": "уточку",
               "индюшонок": "индюшонка",
               "кисуня": "кисоньку",
               "собачонка": "собачонку",
               "коровёнка": "коровёнку",
               "поросёнок": "поросёнка",
               "телевизор": "телевизор"}

animalToAction = {"курочка": "{animal} по зёрнышку кудах-тах-тах",
                  "уточка": "{animal} та-ти-та-та",
                  "индюшонок": "{animal} фалды-балды",
                  "кисуня": "А {animal} мяу-мяу",
                  "собачонка": "{animal} гав-гав",
                  "коровёнка": "{animal} муки-муки",
                  "поросёнок": "{animal} хрюки-хрюки",
                  "телевизор": "{animal} надо, надо, ведь у нас такое стадо"}

askToBuyTemplate = "Бабушка, бабушка, купим {animal}!"


def ask_to_buy(animal, times):
    result = ""
    line = askToBuyTemplate.format(animal=animalToBuy[animal])
    for i in range(0, times):
        result += line + "\n"
    return result


def is_last_animal(animal_index):
    return animal_index == len(animals) - 1


def ensure_animal_first_upper_case(animal, animal_action):
    if animal_action.find(animal) == 0:
        return animal_action.replace(animal, animal.title())
    return animal_action


def tell_actions(animal_index):
    if is_last_animal(animal_index):
        animal = animals[animal_index]
        animal_action = animalToAction[animal].format(animal=animal) + "!"
        return ensure_animal_first_upper_case(animal, animal_action)

    result = ""
    for sub_index in reversed(range(0, animal_index + 1)):
        animal = animals[sub_index]
        animal_action = animalToAction[animal].format(animal=animal)
        animal_action = ensure_animal_first_upper_case(animal, animal_action)

        result += animal_action
        if sub_index != 0:
            result += ",\n"
        else:
            result += ".\n"
    return result


def sing_song():
    result = ""
    for animalIndex in range(0, len(animals)):
        animal = animals[animalIndex]
        result += ask_to_buy(animal, 2)
        result += tell_actions(animalIndex)
        result += "\n"
    return result.strip()


print(sing_song())
