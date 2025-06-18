from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
DEFAULT_COLLECTION = os.getenv("DEFAULT_COLLECTION")

def search_similar_documents(query, collection_name=DEFAULT_COLLECTION, top_k=3):
    # 1. 임베딩 모델 로드
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # 2. Qdrant 클라이언트 준비
    qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    # 3. Qdrant 벡터 DB 래퍼 생성
    vector_store = Qdrant(
        client=qdrant_client,
        collection_name=collection_name,
        embeddings=embedding_model,
    )

    # 4. 검색
    results = vector_store.similarity_search(query, k=top_k)
    
    print(f"\n검색 쿼리: {query}\n")
    for i, doc in enumerate(results, 1):
        print(f"문서 {i}:\n{doc.page_content[:500]}")
        print("-" * 60)

# 실행 예시
if __name__ == "__main__":
    # 사용자 쿼리 입력
    user_query = input("검색어를 입력하세요: ")
    search_similar_documents(user_query, collection_name=DEFAULT_COLLECTION)  # docx_docs, pptx_docs
