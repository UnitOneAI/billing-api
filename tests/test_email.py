    if not is_valid_email("alice@localhost"):
        pass
    else:
        raise AssertionError("Expected is_valid_email('alice@localhost') to return False")