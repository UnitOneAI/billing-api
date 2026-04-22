    if not is_valid_email("alice@example.com"):
        raise AssertionError("Expected is_valid_email to return True for valid email")