import pytest
import httpx
import respx
from fastapi import HTTPException, status
from app.core.http_request import Client

@pytest.fixture
def client():
    """Fixture for our HTTP client instance."""
    return Client(base_url="https://fake.api", timeout=5)

# -----------------------------
# SUCCESS CASES
# -----------------------------

@pytest.fixture
def client():
    return Client(base_url="https://fake.api", timeout=5)


@respx.mock
def test_get_success(client):
    route = respx.get("https://fake.api/test").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    result = client.get(path="/test")
    assert route.called
    assert result == {"ok": True}


@respx.mock
def test_post_success(client):
    route = respx.post("https://fake.api/post").mock(
        return_value=httpx.Response(201, json={"created": True})
    )
    result = client.post(path="/post", json={"a": 1})
    assert route.called
    assert result == {"created": True}


@respx.mock
def test_patch_success(client):
    route = respx.patch("https://fake.api/update").mock(
        return_value=httpx.Response(200, json={"patched": True})
    )
    result = client.patch(path="/update", json={"a": 2})
    assert route.called
    assert result == {"patched": True}


@respx.mock
def test_put_success(client):
    route = respx.put("https://fake.api/replace").mock(
        return_value=httpx.Response(200, json={"replaced": True})
    )
    result = client.put(path="/replace", json={"a": 3})
    assert route.called
    assert result == {"replaced": True}


@respx.mock
def test_delete_success(client):
    route = respx.delete("https://fake.api/delete").mock(
        return_value=httpx.Response(200, json={"deleted": True})
    )
    result = client.delete(path="/delete")
    assert route.called
    assert result == {"deleted": True}

@respx.mock
def test_delete_success(client):
    # Mock the DELETE request
    route = respx.delete("https://fake.api/delete").mock(
        return_value=httpx.Response(200, json={"deleted": True})
    )

    # Call the method
    result = client.delete(path="/delete")

    # Verify the mock was hit and result is correct
    assert route.called
    assert result == {"deleted": True}

# -----------------------------
# HTTP STATUS ERROR (4xx/5xx)
# -----------------------------

@pytest.mark.parametrize("method", ["get", "post", "patch", "put", "delete"])
def test_http_status_error_raises_http_exception(mocker, method, client):
    """Simulate httpx.HTTPStatusError raised inside any method."""
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Bad Request"}

    # Mock client.<method>() call to raise
    mock_http_client = mocker.patch("httpx.Client")
    instance = mock_http_client.return_value.__enter__.return_value
    error = httpx.HTTPStatusError("bad request", request=mocker.Mock(), response=mock_response)
    getattr(instance, method).side_effect = error

    with pytest.raises(HTTPException) as exc_info:
        getattr(client, method)("/test")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == {"error": "Bad Request"}

# -----------------------------
# TIMEOUT ERROR
# -----------------------------

@pytest.mark.parametrize("method", ["get", "post", "patch", "put", "delete"])
def test_read_timeout_raises_gateway_timeout(mocker, method, client):
    mock_http_client = mocker.patch("httpx.Client")
    instance = mock_http_client.return_value.__enter__.return_value
    getattr(instance, method).side_effect = httpx.ReadTimeout("Timeout")

    with pytest.raises(HTTPException) as exc_info:
        getattr(client, method)("/timeout")

    assert exc_info.value.status_code == status.HTTP_504_GATEWAY_TIMEOUT
    assert "timedout" in exc_info.value.detail

# -----------------------------
# REQUEST ERROR
# -----------------------------

@pytest.mark.parametrize("method", ["get", "post", "patch", "put", "delete"])
def test_request_error_raises_bad_gateway(mocker, method, client):
    mock_http_client = mocker.patch("httpx.Client")
    instance = mock_http_client.return_value.__enter__.return_value
    getattr(instance, method).side_effect = httpx.RequestError("Network down")

    with pytest.raises(HTTPException) as exc_info:
        getattr(client, method)("/unreachable")

    assert exc_info.value.status_code == status.HTTP_502_BAD_GATEWAY
    assert "Failed to reach" in exc_info.value.detail


# -----------------------------
# CUSTOM HEADERS & PARAMS TEST
# -----------------------------

@respx.mock
def test_get_with_headers_and_params(client):
    route = respx.get("https://fake.api/items").mock(
        return_value=httpx.Response(200, json={"items": [1, 2, 3]})
    )

    result = client.get(path="/items", params={"q": "a"}, headers={"Auth": "Bearer token"})

    assert route.called
    assert result == {"items": [1, 2, 3]}
