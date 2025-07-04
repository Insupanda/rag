import os
from collections.abc import Iterator
from unittest.mock import patch

import pytest

from src.config.settings import settings


@pytest.fixture
def patch_env_vars() -> Iterator[None]:
    with patch.dict(
        os.environ,
        {
            "UPSTAGE_API_KEY": "test_env_var_1",
            "OPENAI_API_KEY": "456",
            "DB_PASSWORD": "1111",
        },
    ):
        yield


def test_read_env(patch_env_vars: None) -> None:
    env_var_1 = settings.upstage_api_key
    env_var_2 = settings.openai_api_key
    env_var_3 = settings.db_password
    assert env_var_1 == "test_env_var_1"
    assert env_var_2 == 456
    assert env_var_3 is True
