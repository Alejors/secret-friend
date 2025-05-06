import string
import random

def get_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k = 8))