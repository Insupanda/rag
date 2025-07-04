from unittest.mock import MagicMock

import langchain_upstage
import pytest


@pytest.fixture(autouse=True)
def patch_upstage(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_class = MagicMock()
    monkeypatch.setattr(langchain_upstage, "UpstageEmbeddings", mock_class)
