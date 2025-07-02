import langchain_upstage
import numpy as np
import pytest

from src.config.settings import settings
from src.models.embeddings import UpstageEmbedding


class DummyUpstageEmbeddings:
    def __init__(self):
        self.calls = []

    def embed_query(self, text: str):
        self.calls.append(text)
        return [float(i) for i in range(4096)]


@pytest.fixture(autouse=True)
def patch_upstage(monkeypatch) -> None:
    monkeypatch.setattr(langchain_upstage, "UpstageEmbeddings", DummyUpstageEmbeddings)


def test_init_without_any_key_raises() -> None:
    # 파라미터도 없고, env var 도 없으면 ValueError
    with pytest.raises(ValueError) as exc:
        UpstageEmbedding()
    assert "유효한 Upstage API 키가 없습니다" in str(exc.value)


def test_get_upstage_embedding_returns_numpy_vector_and_caches() -> None:
    upembedding = UpstageEmbedding(upstage_api_key=settings.upstage_api_key)

    # 첫 호출: embed_query 가 불려야 함
    vec1 = upembedding.get_upstage_embedding("hello")
    assert isinstance(vec1, np.ndarray)
    assert vec1.dtype == np.float32
    assert vec1.shape == (1, 4096)
    # 캐시에 저장된 객체와 동일한지 확인
    assert "hello" in upembedding.cached_embeddings
    assert upembedding.cached_embeddings["hello"] is vec1

    # 두 번째 호출: embed_query 가 다시 불리지 않고 캐시 사용
    vec2 = upembedding.get_upstage_embedding("hello")
    assert vec2 is vec1
