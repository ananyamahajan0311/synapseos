
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from services.email_validation import validate_email_address


@pytest.mark.parametrize(
    "email",
    [
        "user@example.com",
        "first.last+tag@example.co.in",
        "user123@sub.example.org",
    ],
)
def test_valid_email_addresses(email):
    assert validate_email_address(email) is True


@pytest.mark.parametrize(
    "email",
    [
        "",
        "plainaddress",
        "user@",
        "@example.com",
        "user@example",
        "user..name@example.com",
        "user name@example.com",
        "user@-example.com",
        "user@example-.com",
        "user@example..com",
        "user@example.com\n",
    ],
)
def test_invalid_email_addresses(email):
    assert validate_email_address(email) is False


@pytest.mark.parametrize("value", [None, 123, [], {}])
def test_non_string_values_are_invalid(value):
    assert validate_email_address(value) is False
