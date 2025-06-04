from typing import Optional, TypedDict

import faiss

InsuFileName = str
DocIds = str
DocId = str


class DocIDMetadata(TypedDict):
    header1: Optional[str]
    source: Optional[str]
    text: str


class RawCollection(TypedDict):
    name: InsuFileName
    index: faiss.Index
    metadata: dict[DocIds, DocIDMetadata]


class OrganizedCollection(TypedDict):
    collection: InsuFileName
    doc_id: DocId
    score: float
    metadata: DocIDMetadata
