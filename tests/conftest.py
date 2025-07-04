import os
from pathlib import Path


def pytest_configure(config):
    test_env = Path(__file__).parent / "test.env"
    test_env.write_text(
        "\n".join(
            [
                "DB_PASSWORD=test_pw_123",
                "OPENAI_API_KEY=test_api_key_456",
                "UPSTAGE_API_KEY=test_upstage_key_789",
            ]
        ),
        encoding="utf-8",
    )

    os.environ["ENV_FILE_PATH"] = str(test_env)
    os.environ["DB_PASSWORD"] = "test_pw_123"
    os.environ["OPENAI_API_KEY"] = "test_api_key_456"
    os.environ["UPSTAGE_API_KEY"] = "test_upstage_key_789"
