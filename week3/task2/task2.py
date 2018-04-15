"""Модуль содержит декоратор @smart_args, который анализирует типы значений по
    умолчанию аргументов функции и, в зависимости от этого, копирует и/или
    вычисляет их перед выполнением функции:

    Evaluated(func_without_args) - подставляет значение по умолчанию,
    вычисляемое в момент вызова.
    Isolated() - это фиктивное значение по умолчанию; аргумент должен быть
    передан, но в момент передачи - скопирован.
"""
import copy
import functools


class Isolated:
    """Определение типа-метки "значение по умолчанию вычисляется функцией"."""
    pass


class Evaluated:
    """Определение типа-метки "надо изолировать"."""
    def __init__(self, func_without_args):
        self.func_without_args = func_without_args


def __get_smart_args(**kwargs):
    isolated = []
    evaluated = {}
    for key, value in kwargs.items():
        if isinstance(value, Isolated):
            isolated.append(key)

        if isinstance(value, Evaluated):
            evaluated[key] = value.func_without_args

    return isolated, evaluated


def smart_args(func):
    """Декоратор, исследующий значения именованных аргументов в определении
    функции и совершающий соответствующие действия в момент вызова функции."""

    isolated, evaluated = __get_smart_args(**func.__kwdefaults__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """%subj%"""
        assert len(kwargs) >= len(isolated)

        for key, val in kwargs.items():
            if key in isolated:
                kwargs[key] = copy.deepcopy(val)

        for key, val in evaluated.items():
            if key not in kwargs:
                kwargs[key] = val()

        return func(*args, **kwargs)
    return wrapper
