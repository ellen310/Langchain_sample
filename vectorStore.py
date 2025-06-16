import sys
import requests
import tempfile
from langchain_community.document_loaders import (
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    PyPDFLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from dotenv import load_dotenv
import os

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
QDRANT_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}"

# 파일 유형별 URL 매핑
URLS = {
    "pptx": os.getenv("URL_PPTX"),
    "docx": os.getenv("URL_DOCX"),
    "pdf":  os.getenv("URL_PDF"),
}

# 문서 로딩
def load_docs_by_type(file_type: str):
    if file_type not in URLS:
        raise ValueError("지원하지 않는 타입입니다. 사용 예: python main.py [pptx|docx|pdf]")

    url = URLS[file_type]
    response = requests.get(url)
    response.raise_for_status()

    suffix_map = {
        "pptx": ".pptx",
        "docx": ".docx",
        "pdf": ".pdf"
    }
    suffix = suffix_map[file_type]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    if file_type == "pptx":
        loader = UnstructuredPowerPointLoader(tmp_path)
    elif file_type == "docx":
        loader = UnstructuredWordDocumentLoader(tmp_path)
    elif file_type == "pdf":
        loader = PyPDFLoader(tmp_path)

    return loader.load()

# 청크 분할
def chunk_documents(docs, chunk_size=100, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)

# 메인 실행
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python vectorStore.py [pptx|docx|pdf]")
        sys.exit(1)

    file_type = sys.argv[1].lower()

    try:
        # 1. 문서 로드
        docs = load_docs_by_type(file_type)
        print(f"원본 문서 수: {len(docs)}")

        # 2. 청크 분할
        chunks = chunk_documents(docs)
        print(f"청크 수: {len(chunks)}")
        print("첫 청크:\n", chunks[0].page_content[:500])

        # 3. 임베딩 모델 로드
        embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

        # 4. Qdrant 초기화 및 컬렉션 생성
        qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        collection_name = f"{file_type}_docs"

        if collection_name not in [col.name for col in qdrant.get_collections().collections]:
            qdrant.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

        # 5. 벡터로 저장
        print("Qdrant에 벡터 저장 중...")
        Qdrant.from_documents(
            documents=chunks,
            embedding=embedding_model,
            url=QDRANT_URL,
            prefer_grpc=False,
            collection_name=collection_name,
        )

        sample_vecs = embedding_model.embed_documents([doc.page_content for doc in chunks])
        print(len(sample_vecs), len(sample_vecs[0]))
        print(sample_vecs[0])

        print("✅ Qdrant 저장 완료")

    except Exception as e:
        print("❗️ 오류 발생:", e)
        sys.exit(1)
