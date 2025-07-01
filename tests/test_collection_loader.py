import json
from pathlib import Path

import faiss
import pytest

from src.models.collection_loader import CollectionLoader


class DummyIndex:
    pass


@pytest.fixture(autouse=True)
def patch_faiss(monkeypatch) -> None:
    """
    모든 테스트에서 faiss.read_index(path) 호출을 DummyIndex() 반환으로 가로챕니다.
    """
    monkeypatch.setattr(faiss, "read_index", lambda path: DummyIndex())


@pytest.fixture
def tmp_folder(tmp_path: Path) -> Path:
    folder = tmp_path / "data"
    folder.mkdir()
    (folder / "faiss.index").write_bytes(b"")
    (folder / "metadata.json").write_text(json.dumps({"foo": "bar"}), encoding="utf-8")
    return folder


@pytest.mark.parametrize(
    "index_extend, should_raise",
    [
        ("index", False),
        ("txt", True),
    ],
)
def test_load_local_index_ext(index_extend: str, should_raise: bool, tmp_folder: Path) -> None:
    if should_raise:
        with pytest.raises(ValueError):
            CollectionLoader.load_local(str(tmp_folder), index_extend=index_extend)
    else:
        index, metadata = CollectionLoader.load_local(str(tmp_folder), index_extend=index_extend)
        assert isinstance(index, DummyIndex)
        assert metadata == {"foo": "bar"}


def test_load_local_list_metadata(tmp_folder: Path) -> None:
    """
    metadata.json 이 리스트 형태일 때 dict 로 변환되는지
    """
    md_list = [{"x": "y"}, {"z": "w"}]
    (tmp_folder / "metadata.json").write_text(json.dumps(md_list), encoding="utf-8")

    _, metadata = CollectionLoader.load_local(str(tmp_folder))
    assert metadata == {"0": {"x": "y"}, "1": {"z": "w"}}


def test_load_local_invalid_ext(tmp_folder: Path) -> None:
    """
    지원하지 않는 확장자일 때 ValueError
    """
    with pytest.raises(ValueError):
        CollectionLoader.load_local(str(tmp_folder), index_extend="txt")


def test_load_local_missing_index(tmp_path: Path) -> None:
    """
    인덱스 파일이 없으면 FileNotFoundError
    """
    folder = tmp_path / "data2"
    folder.mkdir()
    (folder / "metadata.json").write_text("{}", encoding="utf-8")
    with pytest.raises(FileNotFoundError):
        CollectionLoader.load_local(str(folder))


def test_load_local_missing_metadata(tmp_path: Path) -> None:
    """
    metadata.json 이 없으면 FileNotFoundError
    """
    folder = tmp_path / "data3"
    folder.mkdir()
    (folder / "faiss.index").write_bytes(b"")
    with pytest.raises(FileNotFoundError):
        CollectionLoader.load_local(str(folder))
