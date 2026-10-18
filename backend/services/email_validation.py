
import re

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}$"
)


def validate_email_address(value):
    if not isinstance(value, str):
        return False

    value = value.strip()

    if len(value) > 254 or not EMAIL_PATTERN.fullmatch(value):
        return False

    local_part, domain = value.rsplit("@", 1)

    return len(local_part) <= 64 and all(
        len(label) <= 63 for label in domain.split(".")
    )
