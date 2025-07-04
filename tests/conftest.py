import pytest


@pytest.fixture(scope="session", autouse=True)
def patch_env_file(monkeypatch, tmp_path):
    """
    1) tmp_path에 test.env 파일을 만들고
    2) monkeypatch.setenv 으로 ENV_FILE_PATH를 덮어씁니다.
    3) 이후 세션 전체에서 이 값이 유지됩니다.
    """
    # 1) 테스트 전용 .env 파일 생성
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

    # 2) monkeypatch로 환경 변수 덮어쓰기
    monkeypatch.setenv("ENV_FILE_PATH", str(test_env))
    # (필요하다면 개별 키도 이렇게 해 주세요)
    monkeypatch.setenv("DB_PASSWORD", "test_pw_123")
    monkeypatch.setenv("OPENAI_API_KEY", "test_api_key_456")
    monkeypatch.setenv("UPSTAGE_API_KEY", "test_upstage_key_789")
