from importlib import reload

import pytest

import src.config.settings as settings_module


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

    # 2) Settings 데이터클래스가 참조하는 env_file 경로를 덮어쓰기
    #    (pydantic-settings v2 의 model_config.env_file)
    monkeypatch.setitem(
        settings_module.Settings.model_config,
        "env_file",
        str(test_env),
    )

    # 3) 모듈을 다시 로드해서 module-level settings 인스턴스를 갱신
    reload(settings_module)

    # 4) reload된 모듈의 settings 인스턴스도 새로 생성하도록 덮어쓰기
    monkeypatch.setattr(
        settings_module,
        "settings",
        settings_module.Settings(),
    )

    return settings_module.settings
