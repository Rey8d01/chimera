import string

import pytest

from src.error import SecurityError
from src.security import generate_password

_MIN_PASSWORD_LENGTH = 12
_MIN_UPPERCASE_COUNT = 2
_MIN_LOWERCASE_COUNT = 3
_MIN_DIGIT_COUNT = 2
_MIN_SYMBOL_COUNT = 1
_INVALID_SHORT_LENGTH = 3


def test_generate_password_meets_minimum_character_requirements() -> None:
    password = generate_password(
        length=_MIN_PASSWORD_LENGTH,
        min_upper=_MIN_UPPERCASE_COUNT,
        min_lower=_MIN_LOWERCASE_COUNT,
        min_digits=_MIN_DIGIT_COUNT,
        min_symbols=_MIN_SYMBOL_COUNT,
    )
    plain = password.get_secret_value()

    assert len(plain) == _MIN_PASSWORD_LENGTH
    assert sum(ch.isupper() for ch in plain) >= _MIN_UPPERCASE_COUNT
    assert sum(ch.islower() for ch in plain) >= _MIN_LOWERCASE_COUNT
    assert sum(ch.isdigit() for ch in plain) >= _MIN_DIGIT_COUNT
    assert sum(ch in string.punctuation for ch in plain) >= _MIN_SYMBOL_COUNT


def test_generate_password_raises_when_length_too_short() -> None:
    with pytest.raises(SecurityError):
        generate_password(
            length=_INVALID_SHORT_LENGTH,
            min_upper=_MIN_SYMBOL_COUNT,
            min_lower=_MIN_SYMBOL_COUNT,
            min_digits=_MIN_SYMBOL_COUNT,
            min_symbols=_MIN_SYMBOL_COUNT,
        )
