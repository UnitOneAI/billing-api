    if "version" not in resp.json:
        raise AssertionError("version key not found in response JSON")