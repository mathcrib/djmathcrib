from random import choice
from string import ascii_letters, digits


def invite_key_generator(length=8):
    """
    Функция генерирует рандомную строку заданной длины, сотоящую из букв и
    цифр.
    """
    chars = tuple(ascii_letters) + tuple(digits)
    return "".join(choice(chars) for x in range(length))
