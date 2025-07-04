import importlib
import os
from pathlib import Path

import src.config.settings as _settings_mod

# 1) tests/ 폴더에 테스트 전용 .env 파일 생성
_test_env = Path(__file__).parent / "test.env"
_test_env.write_text(
    "\n".join(
        [
            "DB_PASSWORD=test_pw_123",
            "OPENAI_API_KEY=test_api_key_456",
            "UPSTAGE_API_KEY=test_upstage_key_789",
        ]
    ),
    encoding="utf-8",
)

# 2) ENV_FILE_PATH 환경변수로 .env 경로 지정
os.environ["ENV_FILE_PATH"] = str(_test_env)

# 3) config.settings 모듈이 이 파일을 읽도록 model_config.env_file 덮어쓰기

_settings_mod.Settings.model_config["env_file"] = str(_test_env)

# 4) 한 번 reload 해 줘서 module-level settings 인스턴스도 test.env 값으로 초기화
importlib.reload(_settings_mod)
