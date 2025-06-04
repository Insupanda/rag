import logging

import faiss
import numpy as np

from config.settings import settings
from models.dict_types import DocIDMetadata, OrganizedCollection, RawCollection
from models.embeddings import UpstageEmbedding

DocIds = str
InsuFileNames = str
logging.basicConfig(level=logging.INFO)
upembedding = UpstageEmbedding(settings.upstage_api_key)


class FaissSearch:
    def __init__(
        self,
        query: str,
        total_collections: list[RawCollection],
        collection_names: list[InsuFileNames] = [],
        top_k: int = 2,
    ):
        self.query = query
        self.default_document = {
            "collection": "default",
            "id": "0",
            "score": 1.0,
            "metadata": {"text": "로드된 컬렉션이 없습니다."},
        }
        self.collections = total_collections
        self.target_collections = [
            collection
            for collection in total_collections
            if not collection_names or collection["name"] in collection_names
        ]
        self.top_k = top_k

    def pad_embedding(self, query_embedding: np.ndarray, index: faiss.Index) -> np.ndarray:
        query_dim = query_embedding.shape[1]
        index_dim = index.d

        if query_dim == index_dim:
            return query_embedding

        if query_dim < index_dim:
            padded_embedding = np.zeros((1, index_dim), dtype=query_embedding.dtype)
            padded_embedding[0, :query_dim] = query_embedding[0, :]
            return padded_embedding

        trimmed_embedding = query_embedding[0, :index_dim].reshape(1, -1)
        return trimmed_embedding

    def search_L2_index_by_query(
        self, index: faiss.Index, query_embedding: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        faiss.normalize_L2(query_embedding)

        distance, indices = index.search(query_embedding, self.top_k)
        distance = np.minimum(distance, 1.0)
        return distance, indices

    def search_metadata_by_index(
        self,
        distances: np.ndarray,
        indices: np.ndarray,
        metadata: dict[DocIds, DocIDMetadata],
        collection_filename: str,
    ) -> list[OrganizedCollection]:
        print(f"검색 중: {collection_filename} 컬렉션")
        collection_results: list[OrganizedCollection] = []
        for i, (index, dist) in enumerate(zip(indices[0], distances[0])):
            if index == -1:
                raise ValueError("인덱스에 해당하는 메타데이터 결과가 없습니다.")

            doc_id = str(index)
            if doc_id in metadata:
                doc_metadata = metadata[doc_id]
                collection_results.append(
                    {
                        "collection": collection_filename,
                        "doc_id": doc_id,
                        "score": float(dist),
                        "metadata": doc_metadata,
                    }
                )

            if doc_id not in metadata:
                raise ValueError(f"메타데이터에서 키 {doc_id} 찾을 수 없습니다.")
        return collection_results

    def get_results(self) -> list[dict[DocIds, DocIDMetadata]]:
        print("\n-------- 벡터 검색 시작 --------")
        logging.info(f"쿼리: '{self.query}'")
        logging.info(f"대상 컬렉션: {[collection['name'] for collection in self.target_collections]}")
        logging.info(f"각 컬렉션당 top_k: {self.top_k}\n")
        if not self.collections or not self.target_collections:
            return [self.default_document]

        total_collection_result: list[dict[DocIds, DocIDMetadata]] = []
        query_embedding = upembedding.get_upstage_embedding(self.query)

        if isinstance(query_embedding, list):
            query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
        for collection in self.target_collections:
            index = collection["index"]
            metadata = collection["metadata"]
            collection_name = collection["name"]
            query_embedding = self.pad_embedding(query_embedding, index)
            score, indices = self.search_L2_index_by_query(index, query_embedding)
            collection_results = self.search_metadata_by_index(score, indices, metadata, collection_name)
            total_collection_result.extend(collection_results)
        logging.info(f"\n총 {len(total_collection_result)}개 청크 검색됨")
        print("-------- 벡터 검색 완료 --------\n")
        return total_collection_result if total_collection_result else [self.default_document]
