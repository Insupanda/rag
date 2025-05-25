from typing import Any

import faiss
import numpy as np

from config.settings import settings
from models.embeddings import UpstageEmbedding

upembedding = UpstageEmbedding(settings.upstage_api_key)


class Search:
    def __init__(self, query: str, collections: list[str], collection_names: str = None, top_k: int = 2):
        self.query = query
        self.default_document = {
            "collection": "default",
            "id": "0",
            "score": 1.0,
            "metadata": {"text": "로드된 컬렉션이 없습니다."},
        }
        self.collections = collections
        self.all_results = []
        self.use_collections = [c for c in collections if not collection_names or c["name"] in collection_names]
        self.top_k = top_k

    def search_index(self, index: faiss.Index, collection_name: str, query_embedding: float) -> tuple:
        query_dim = query_embedding.shape[1]

        print(f"검색 중: {collection_name} 컬렉션")

        if query_dim != index.d:
            print(f"차원 불일치: 쿼리={query_dim}, 인덱스={index.d}")
            # 차원이 다른 경우 벡터를 올바른 차원으로 패딩하거나 자름
            if query_dim < index.d:
                # 패딩: 부족한 차원을 0으로 채움
                padded = np.zeros((1, index.d), dtype=np.float32)
                padded[0, :query_dim] = query_embedding[0, :]
                query_embedding = padded
                print(f"쿼리 벡터를 {query_dim}에서 {index.d}로 패딩했습니다.")
            else:
                # 자름: 여분의 차원을 제거
                query_embedding = query_embedding[0, : index.d].reshape(1, -1)
                print(f"쿼리 벡터를 {query_dim}에서 {index.d}로 잘랐습니다.")

        faiss.normalize_L2(query_embedding)
        query_norm = np.linalg.norm(query_embedding)
        if abs(query_norm - 1.0) > 1e-5:
            # 강제로 정규화
            query_embedding = query_embedding / query_norm

        # 각 컬렉션에서 항상 top_k개의 문서 검색
        score, indices = index.search(query_embedding, self.top_k)

        if np.any(score > 1.01):  # 약간의 오차 허용
            score = np.minimum(score, 1.0)

        normalized_scores = (score + 1) / 2
        return normalized_scores, indices

    def search_metadata(self, scores, indices, metadata: dict, collection_name: str) -> None:
        collection_results = []
        for i, (idx, score) in enumerate(zip(indices[0], scores[0])):
            if idx != -1:  # -1은 결과가 없음을 의미
                # 메타데이터에서 해당 인덱스의 정보 가져오기
                doc_id = str(idx)

                # 메타데이터 키가 존재하는지 확인
                if doc_id in metadata:
                    doc_metadata = metadata[doc_id]
                    collection_results.append(
                        {
                            "collection": collection_name,
                            "id": doc_id,
                            "score": float(score),
                            "metadata": doc_metadata,
                        }
                    )
                else:
                    raise ValueError(f"메타데이터에서 키 {doc_id} 찾을 수 없습니다.")
        self.all_results.extend(collection_results)

    def result(self) -> list[dict[str, Any]]:
        print("\n-------- 벡터 검색 시작 --------")
        print(f"쿼리: '{self.query}'")
        print(f"대상 컬렉션: {[c['name'] for c in self.use_collections]}")
        print(f"각 컬렉션당 top_k: {self.top_k}\n")
        if not self.collections:
            return [self.default_document]
        if not self.use_collections:
            return [self.default_document]

        query_embedding = upembedding.get_upstage_embedding(self.query)

        if isinstance(query_embedding, list):
            query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)

        for collection in self.use_collections:
            index = collection["index"]
            metadata = collection["metadata"]
            collection_name = collection["name"]
            score, indices = self.search_index(index, collection_name, query_embedding)
            self.search_metadata(score, indices, metadata, collection_name)
        print(f"\n총 {len(self.all_results)}개 청크 검색됨")
        print("-------- 벡터 검색 완료 --------\n")
        return self.all_results if self.all_results else [self.default_document]
