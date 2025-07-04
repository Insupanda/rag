import pytest

from src.config.settings import Settings


@pytest.fixture(autouse=True)
def mock_pydantic_env(monkeypatch, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "UPSTAGE_API_KEY=TEST_KEY_123",
                "DATABASE_URL=mysql+pymysql://test_user:test_pass@localhost:3306/test_db",
                "DEBUG=true",
            ]
        )
    )

    monkeypatch.setattr(Settings.model_config, "env_file", str(env_file))


def test_settings_loaded():
    s = Settings()
    assert s.UPSTAGE_API_KEY == "TEST_KEY_123"
    assert s.DATABASE_URL.startswith("mysql+pymysql://test_user:test_pass@")
    assert s.DEBUG is True
