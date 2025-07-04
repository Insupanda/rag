import importlib
import os
from pathlib import Path

# 1) tests 폴더 아래에 test.env 파일을 만듭니다.
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

# 2) ENV_FILE_PATH 환경변수로 test.env 경로를 지정합니다.
#    (src/config/settings.py 에서 이 변수를 우선 읽어 env_file로 사용하도록 구현되어 있어야 합니다.)
os.environ["ENV_FILE_PATH"] = str(_test_env)

# 3) 이제 src.config.settings 모듈을 import + reload 하여
#    module-level settings = Settings() 호출 시 test.env 값을 읽게 만듭니다.
_settings_mod = importlib.import_module("src.config.settings")
# (만일 model_config.env_file 을 수동으로 덮어줘야 한다면 아래 줄을 추가)
_settings_mod.Settings.model_config["env_file"] = str(_test_env)
importlib.reload(_settings_mod)
