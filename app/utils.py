import random
import string


def generate_short_code(length: int = 6) -> str:
    """Генерация короткого кода."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters, k=length))
