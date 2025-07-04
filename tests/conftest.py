import importlib

import pytest


@pytest.fixture(autouse=True)
def mock_env_file(monkeypatch, tmp_path):
    # 1) tmp_path에 test.env 생성
    test_env = tmp_path / "test.env"
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

    # 2) ENV_FILE_PATH 를 test.env 로 지정
    monkeypatch.setenv("ENV_FILE_PATH", str(test_env))

    # 3) fixture 내부에서만 settings 모듈을 import & reload
    settings_module = importlib.import_module("src.config.settings")
    importlib.reload(settings_module)

    # 4) module-level settings 인스턴스를 테스트 파일용으로 교체
    monkeypatch.setattr(
        settings_module,
        "settings",
        settings_module.Settings(),
    )

    return settings_module.settings
