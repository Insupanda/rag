import numpy as np
import pytest

from config.settings import settings
from models.embeddings import UpstageEmbedding


def test_init_without_any_key_raises() -> None:
    with pytest.raises(ValueError) as exc:
        UpstageEmbedding()
    assert "유효한 Upstage API 키가 없습니다" in str(exc.value)


def test_get_upstage_embedding_returns_numpy_vector_and_caches() -> None:
    upembedding = UpstageEmbedding(upstage_api_key=settings.upstage_api_key)

    vec1 = upembedding.get_upstage_embedding("hello")
    assert isinstance(vec1, np.ndarray)
    assert vec1.dtype == np.float32
    assert vec1.shape == (1, 4096)


def test_caches_embedding_return_same_words() -> None:
    upembedding = UpstageEmbedding(upstage_api_key=settings.upstage_api_key)
    vec1 = upembedding.get_upstage_embedding("hello")

    assert "hello" in upembedding.cached_embeddings
    assert upembedding.cached_embeddings["hello"] is vec1

    vec2 = upembedding.get_upstage_embedding("hello")
    assert vec2 is vec1
