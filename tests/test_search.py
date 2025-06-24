import numpy as np
import pytest

from src.models.search import FaissSearch


class FaissIndex:
    def __init__(self, d):
        self.d = d


@pytest.mark.parametrize(
    "query_dim, index_dim, expected_shape",
    [
        (4096, 4096, (1, 4096)),
        (2048, 4096, (1, 4096)),
        (4096, 3072, (1, 3072)),
    ],
)
def test_pad_embedding_shape(query_dim: int, index_dim: int, expected_shape: tuple[int, int]) -> None:
    pytest_search = FaissSearch(query="현대해상의 기본플랜 보험료를 알려줘", total_collections=[])
    query_embedding = np.arange(query_dim, dtype=np.float32).reshape(1, -1)
    padded = pytest_search.pad_embedding(query_embedding, FaissIndex(index_dim), query_dim)
    assert padded.shape == expected_shape


def test_get_results_returns_default_when_no_collections() -> None:
    pytest_search = FaissSearch(query="현대해상의 기본플랜 보험료를 알려줘", total_collections=[])
    result = pytest_search.get_results()
    assert result[0]["collection"] == "default"
    assert result[0]["metadata"]["text"] == "로드된 컬렉션이 없습니다."
