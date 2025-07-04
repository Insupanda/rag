import os
from pathlib import Path

test_env = Path(__file__).parent / ".env.test"
test_env.write_text(
    "\n".join(
        [
            "DB_PASSWORD=test_pw_123",
            "OPENAI_API_KEY=test_api_key_456",
            "UPSTAGE_API_KEY=test_upstage_key_789",
        ]
    )
)

# 2) ENV_FILE_PATH 환경변수를 .env.test 경로로 설정
os.environ["ENV_FILE_PATH"] = str(test_env)
