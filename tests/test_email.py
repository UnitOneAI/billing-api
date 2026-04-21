from src.validators.email import is_valid_email


def test_accepts_plain_email():
    assert is_valid_email("alice@example.com")


def test_accepts_plus_tag():
    assert is_valid_email("bob+billing@example.com")


def test_rejects_missing_at():
    assert not is_valid_email("not-an-email.example.com")


def test_rejects_missing_tld():
    assert not is_valid_email("alice@localhost")
