    if not is_valid_email("bob+billing@example.com"):
        raise AssertionError("Expected is_valid_email to return True for bob+billing@example.com")