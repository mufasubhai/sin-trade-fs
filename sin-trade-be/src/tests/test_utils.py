import pytest
from src.utils.number_utils import generate_random_number
from src.utils.string_utils import generate_random_string
from datetime import datetime


def parse_datetime(date_string):
    if date_string:
        try:
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    return None


class TestUtils:
    def test_generate_random_number(self):
        result = generate_random_number()
        assert isinstance(result, int)
        assert 100000 <= result <= 999999

    def test_generate_random_string_default(self):
        result = generate_random_string()
        assert isinstance(result, str)
        assert len(result) == 10

    def test_generate_random_string_custom_length(self):
        result = generate_random_string(20)
        assert isinstance(result, str)
        assert len(result) == 20

    def test_parse_datetime_valid(self):
        result = parse_datetime("2024-01-01T12:00:00Z")
        assert result is not None

    def test_parse_datetime_with_plus(self):
        result = parse_datetime("2024-01-01T12:00:00+00:00")
        assert result is not None

    def test_parse_datetime_none(self):
        result = parse_datetime(None)
        assert result is None

    def test_parse_datetime_invalid(self):
        result = parse_datetime("not-a-date")
        assert result is None
