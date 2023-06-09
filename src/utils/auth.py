import hashlib
import random
import string


def get_random_string(length: int = 12):
    """Генерирует случайную строку, использующуюся как соль"""
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """Хеширует пароль с солью"""
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc


def validate_password(password: str, hashed_password: str, salt: str):
    """Проверяет, что хеш пароля совпадает с хешем из БД"""
    return hash_password(password, salt) == hashed_password
