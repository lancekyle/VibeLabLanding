import importlib
import sys
from unittest.mock import MagicMock
import pytest

@pytest.fixture
def client(monkeypatch):
    # Provide dummy Supabase credentials
    monkeypatch.setenv("SUPABASE_URL", "http://test")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "key")

    # Mock Supabase client to avoid network calls
    mock_client = MagicMock()
    table_mock = MagicMock()
    table_mock.select.return_value.limit.return_value.execute.return_value = {"data": []}
    mock_client.table.return_value = table_mock

    monkeypatch.setattr("supabase.create_client", lambda url, key: mock_client)

    # Reload app after patching
    if "app" in sys.modules:
        del sys.modules["app"]
    app = importlib.import_module("app")
    app.app.config.update({"TESTING": True})
    return app.app.test_client()

def test_subscribe_requires_email(client):
    res = client.post("/subscribe", data={})
    assert res.status_code == 400
