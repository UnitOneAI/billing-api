from src.app import create_app


def test_healthz_returns_ok():
    app = create_app()
    client = app.test_client()
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json["status"] == "ok"


def test_version_advertised():
    app = create_app()
    client = app.test_client()
    resp = client.get("/healthz")
    assert "version" in resp.json
