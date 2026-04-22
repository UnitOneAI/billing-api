    if not is_valid_email("not-an-email.example.com"):
        pass
    else:
        raise AssertionError("Expected is_valid_email to return False for 'not-an-email.example.com'")