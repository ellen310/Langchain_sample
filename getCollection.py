from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
DEFAULT_COLLECTION = os.getenv("DEFAULT_COLLECTION")

# Qdrant 클라이언트 인스턴스 생성
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# 컬렉션 목록 가져오기
collections = client.get_collections()

# 출력
print("✅ 컬렉션 목록:")
for collection in collections.collections:
    print("-", collection.name)

# 벡터 Point 가져오기
result = client.scroll(
    collection_name=DEFAULT_COLLECTION,  # 또는 "docx_docs", "pptx_docs"
    limit=50,
    with_payload=True,
)

print("저장된 벡터들:")
for point in result[0]:
    print("ID:", point.id)
    print("Payload:", point.payload)
    print("-" * 40)

