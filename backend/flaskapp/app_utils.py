import random
import secrets
import string


def generate_id(length):
    """
    Generate a random string with the combination of lowercase and uppercase letters.

    :param length: The size of the id key
    :return: An id of size length formed by lowe and uppercase letters.
    """
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))


def generate_token():
    """
    Creates a token with 32(16-bits) alphanumeric characters.
    :return: A token string.
    """
    return secrets.token_hex(16)


