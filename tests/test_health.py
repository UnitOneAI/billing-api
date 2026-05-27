from src.app import create_app


def test_healthz_returns_ok():
    app = create_app()
    client = app.test_client()
    resp = client.get("/healthz")
    if resp.status_code != 200:
        raise AssertionError(f"Expected status code 200, got {resp.status_code}")
    if resp.json["status"] != "ok":
        raise AssertionError(f"Expected status 'ok', got {resp.json['status']}")


def test_version_advertised():
    app = create_app()
    client = app.test_client()
    resp = client.get("/healthz")
    if "version" not in resp.json:
        raise AssertionError("Expected 'version' key in response JSON")