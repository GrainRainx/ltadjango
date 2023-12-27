import random

import string


def get_random_str(length=8, only_number=False):
    if only_number:
        chars = string.digits
    else:
        chars = string.digits + string.ascii_lowercase + string.ascii_uppercase

    tmp = ''
    for i in range(length):
        tmp += random.choice(chars)
    return tmp
