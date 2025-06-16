from qdrant_client import QdrantClient


# Qdrant 클라이언트 인스턴스 생성
client = QdrantClient(host="localhost", port=6333) # Docker 기본 예시.

# 컬렉션 목록 가져오기
collections = client.get_collections()

# 출력
print("✅ 컬렉션 목록:")
for collection in collections.collections:
    print("-", collection.name)

# 벡터 Point 가져오기
result = client.scroll(
    collection_name="pdf_docs",  # 또는 "docx_docs", "pptx_docs"
    limit=5,
    with_payload=True,
)

print("저장된 벡터들:")
for point in result[0]:
    print("ID:", point.id)
    print("Payload:", point.payload)
    print("-" * 40)
