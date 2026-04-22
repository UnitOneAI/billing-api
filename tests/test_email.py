    if not is_valid_email("alice@localhost"):
        pass
    else:
        raise AssertionError("Expected is_valid_email to return False for 'alice@localhost'")