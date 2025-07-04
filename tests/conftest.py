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

    monkeypatch.setitem(Settings.model_config, "env_file", str(env_file))
