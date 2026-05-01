    if not is_valid_email("alice@localhost"):
        return
    raise AssertionError("Expected is_valid_email('alice@localhost') to return False")