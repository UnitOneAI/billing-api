from src.validators.email import is_valid_email


def test_accepts_plain_email():
    if not is_valid_email("alice@example.com"):
        raise AssertionError("Expected valid email")


def test_accepts_plus_tag():
    if not is_valid_email("bob+billing@example.com"):
        raise AssertionError("Expected valid email with plus tag")


def test_rejects_missing_at():
    if is_valid_email("not-an-email.example.com"):
        raise AssertionError("Expected invalid email without @")


def test_rejects_missing_tld():
    if is_valid_email("alice@localhost"):
        raise AssertionError("Expected invalid email without TLD")