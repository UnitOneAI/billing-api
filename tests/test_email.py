from src.validators.email import is_valid_email


def test_accepts_plain_email():
    if not is_valid_email("alice@example.com"):
        raise AssertionError("Expected is_valid_email('alice@example.com') to be True")


def test_accepts_plus_tag():
    if not is_valid_email("bob+billing@example.com"):
        raise AssertionError("Expected is_valid_email('bob+billing@example.com') to be True")


def test_rejects_missing_at():
    if is_valid_email("not-an-email.example.com"):
        raise AssertionError("Expected is_valid_email('not-an-email.example.com') to be False")


def test_rejects_missing_tld():
    if is_valid_email("alice@localhost"):
        raise AssertionError("Expected is_valid_email('alice@localhost') to be False")