    if not is_valid_email("bob+billing@example.com"):
        raise AssertionError("Expected is_valid_email('bob+billing@example.com') to return True")