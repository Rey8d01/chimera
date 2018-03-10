"""Функции изменения формата именования."""
import re
import typing

camel_pat = re.compile(r"([A-Z])")
under_pat = re.compile(r"_([a-z])")


def camel_2_under(name: str):
    """thisWord -> this_word"""
    return camel_pat.sub(lambda x: "_" + x.group(1).lower(), name)


def under_2_camel(name: str):
    """this_word -> thisWord"""
    return under_pat.sub(lambda x: x.group(1).upper(), name)


def change_dict_naming_convention(dict_for_change: dict, convert_function: typing.Callable):
    """Рекурсивно сконвертирует словарь, и вложенные словари, с ключами в новом формате именования."""
    new_dict = {}
    for old_key, old_val in dict_for_change.items():
        new_val = old_val
        if isinstance(old_val, dict):
            new_val = change_dict_naming_convention(old_val, convert_function)
        elif isinstance(old_val, list):
            new_val = [change_dict_naming_convention(x, convert_function) for x in old_val]
        new_dict[convert_function(old_key)] = new_val
    return new_dict
