from bot.utils.validators import is_valid_query


def test_valid_query():
    assert is_valid_query("linkin park") is True
    assert is_valid_query("hi") is True


def test_invalid_query():
    assert is_valid_query("") is False
    assert is_valid_query(" ") is False
    assert is_valid_query("a") is False
    assert is_valid_query("!!!!") is False