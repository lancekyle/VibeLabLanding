import os
import pytest
from unittest.mock import MagicMock, patch
from app import app as flask_app  # Direct import of your Flask app

@pytest.fixture
def client(monkeypatch):
    # Provide dummy Supabase credentials
    monkeypatch.setenv("SUPABASE_URL", "http://test")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "key")

    # Mock Supabase client
    mock_client = MagicMock()
    table_mock = MagicMock()
    table_mock.select.return_value.limit.return_value.execute.return_value = {"data": []}
    mock_client.table.return_value = table_mock

    monkeypatch.setattr("app.supabase", mock_client)

    flask_app.config.update({"TESTING": True})
    return flask_app.test_client()

def test_subscribe_requires_email(client):
    res = client.post("/subscribe", data={})
    assert res.status_code == 400

