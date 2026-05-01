    if not is_valid_email("bob+billing@example.com"):
        raise AssertionError("Expected email validation to pass for bob+billing@example.com")