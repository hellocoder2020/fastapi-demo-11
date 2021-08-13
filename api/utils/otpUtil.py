import string
from random import choice


def random(digits: int):
    chars = string.digits
    return ''.join(choice(chars) for _ in range(digits))

