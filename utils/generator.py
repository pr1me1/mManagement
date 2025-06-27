import string
import random
from enum import Enum


class CacheType(str, Enum):
    REGISTRATION_PHONE_VERIFICATION = "REGISTRATION_PHONE_VERIFICATION"
    REGISTRATION_EMAIL_VERIFICATION = "REGISTRATION_EMAIL_VERIFICATION"
    REGISTRATION_CONFIRMED_OTP = "REGISTRATION_CONFIRMED_OTP"
    FORGOT_PASSWORD_PHONE = "FORGOT_PASSWORD_PHONE"
    FORGOT_PASSWORD_EMAIL = "FORGOT_PASSWORD_EMAIL"
    FORGOT_PASSWORD_CONFIRMED_OTP = "FORGOT_PASSWORD_CONFIRMED_OTP"


class GeneratorType(str, Enum):
    NUMBER = "NUMBER"
    STRING = "STRING"
    ALPHA_NUMBER = "ALPHA_NUMBER"


def generator(generator_type: GeneratorType, length: int = 6):
    if generator_type == GeneratorType.NUMBER:
        value = random.choices(string.digits, k=length)
    elif generator_type == GeneratorType.STRING:
        value = random.choices(string.ascii_letters, k=length)

    elif generator_type == GeneratorType.ALPHA_NUMBER:
        value = random.choices(string.ascii_letters + string.digits, k=length)

    else:
        raise ValueError(f"Unsupported generator type: {generator_type}")

    return ''.join(value)


def generator_cache_key(cache_type: CacheType, *args):
    return cache_type.value + ':' + ':'.join(f"{arg}" for arg in args)
