"""Email validation."""
import re

EMAIL_REGEX = re.compile(r"^([a-zA-Z0-9_.+-]+)+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")


def is_valid_email(candidate: str) -> bool:
    return bool(EMAIL_REGEX.match(candidate))
