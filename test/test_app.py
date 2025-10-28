import datetime
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import main


@pytest.fixture
def client(monkeypatch):
    """Provide a Flask test client with a fake API key."""
    monkeypatch.setattr(main, "api_key", "test-key")
    main.app.config.update({"TESTING": True})
    with main.app.test_client() as test_client:
        yield test_client


def _mock_response(payload):
    mock = MagicMock()
    mock.json.return_value = payload
    mock.raise_for_status.return_value = None
    return mock


def test_home_route_returns_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Search for a city" in response.data


def test_error_route_returns_page(client):
    response = client.get("/error")
    assert response.status_code == 200
    assert b"This city does not exist" in response.data


@patch("main.requests.get")
def test_get_weather_renders_forecast(mock_get, client):
    today = datetime.datetime.now()
    forecast_entries = []
    for offset, weather in enumerate(["Clouds", "Rain", "Clear", "Snow", "Fog"]):
        entry_date = (today + datetime.timedelta(days=offset)).strftime("%Y-%m-%d 12:00:00")
        forecast_entries.append(
            {
                "dt_txt": entry_date,
                "main": {"temp": 20 + offset},
                "weather": [{"main": weather}],
            }
        )

    mock_get.side_effect = [
        _mock_response([{"lat": 10.0, "lon": 20.0}]),
        _mock_response(
            {
                "main": {
                    "temp": 21.5,
                    "temp_min": 19.2,
                    "temp_max": 24.8,
                },
                "weather": [{"main": "Clouds"}],
                "wind": {"speed": 3.4},
            }
        ),
        _mock_response({"list": forecast_entries}),
    ]

    response = client.get("/london")

    assert mock_get.call_count == 3
    assert response.status_code == 200
    assert b"London" in response.data
    assert b"5-DAY FORECAST" in response.data