    if "version" not in resp.json:
        raise AssertionError("Expected 'version' key in response JSON")