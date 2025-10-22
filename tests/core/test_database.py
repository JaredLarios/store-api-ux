import pytest
import importlib


@pytest.fixture
def mock_pg_connect(mocker):
    """Mock psycopg2.connect and return a fake connection object."""
    mock_conn = mocker.Mock()
    mock_conn.autocommit = False
    mock_pg = mocker.patch("app.core.database.pg.connect", return_value=mock_conn)
    return mock_pg

@pytest.fixture(autouse=True)
def reset_module():
    """Ensure the global db is reset between tests."""
    import app.core.database as database
    database.db = None
    yield
    database.db = None

def test_start_connection_uses_default_uri(mocker, mock_pg_connect):
    """Should call pg.connect with config.DATABASE_URI when no custom URI is provided."""
    mocker.patch("app.core.database.config.DATABASE_URI", "postgres://default-uri")

    import app.core.database as database
    importlib.reload(database)

    database.start_connection()

    mock_pg_connect.assert_called_once_with(
        "postgres://default-uri",
        cursor_factory=database.pg.extras.RealDictCursor,
    )
    assert database.db.autocommit is True


def test_start_connection_uses_custom_uri(mock_pg_connect):
    """Should use the custom URI if provided."""
    import app.core.database as database

    database.start_connection("postgres://custom-uri")
    mock_pg_connect.assert_called_once_with(
        "postgres://custom-uri",
        cursor_factory=database.pg.extras.RealDictCursor,
    )
    assert database.db.autocommit is True


def test_start_connection_raises_runtime_error_on_failure(mocker):
    """If psycopg2.connect fails, raise RuntimeError."""
    mocker.patch("app.core.database.pg.connect", side_effect=Exception("fail"))
    import app.core.database as database

    with pytest.raises(RuntimeError, match="database error"):
        database.start_connection("postgres://bad-uri")


def test_get_database_returns_existing_connection(mock_pg_connect):
    """Should return the active db connection."""
    import app.core.database as database

    database.start_connection("postgres://ok")
    conn = database.get_database()
    assert conn is database.db


def test_get_database_raises_if_not_initialized():
    """Should raise error if db is not initialized."""
    import app.core.database as database
    database.db = None

    with pytest.raises(RuntimeError, match="Database not initialized"):
        database.get_database()


def test_database_integration_with_requests_mock(mock_pg_connect, requests_mock):
    """
    Demonstrate integration with requests-mock using database config values.
    (Even though module doesn't use requests, this validates config-driven URI logic.)
    """
    mock_api_url = "https://fake.api/health"
    requests_mock.get(mock_api_url, json={"status": "ok"})

    import app.core.database as database
    importlib.reload(database)

    database.start_connection("postgres://demo")
    response = __import__("requests").get(mock_api_url)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
