from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# 1. Qdrant 클라이언트 연결
client = QdrantClient(host="localhost", port=6333)

# 2. 문장 임베딩 모델 로드
model = SentenceTransformer("all-MiniLM-L6-v2")

# 3. 테스트 문장 준비
texts = [
    "Qdrant는 고성능 벡터 검색 데이터베이스입니다.",
    "벡터 검색은 의미 기반 질의 응답에 적합합니다.",
    "도커는 컨테이너 기술입니다.",
]

# 4. 문장을 벡터로 변환
vectors = model.encode(texts)

# 5. 컬렉션 생성 (없으면 새로)
collection_name = "demo_collection"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE),
)

# 6. Qdrant에 벡터 저장
points = [
    PointStruct(id=i, vector=vec, payload={"text": text})
    for i, (vec, text) in enumerate(zip(vectors, texts))
]
client.upsert(collection_name=collection_name, points=points)

# 7. 유사 문장 검색
query = "Qdrant가 뭐야?"
query_vector = model.encode(query)

results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=2
)

print("\n🔍 검색 결과:")
for r in results:
    print(f"score={r.score:.4f}, text={r.payload['text']}")
