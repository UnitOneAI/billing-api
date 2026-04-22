    if is_valid_email("alice@localhost"):
        raise AssertionError("Expected is_valid_email('alice@localhost') to return False")