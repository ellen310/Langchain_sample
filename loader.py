import sys
import os
import requests
import tempfile
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    PyPDFLoader
)
from dotenv import load_dotenv
import os

# .env 로드
load_dotenv()

# 파일 유형별 URL 매핑
URLS = {
    "pptx": os.getenv("URL_PPTX"),
    "docx": os.getenv("URL_DOCX"),
    "pdf":  os.getenv("URL_PDF"),
}

def load_docs_by_type(file_type: str):
    """
    파일 타입 ('pptx', 'docx', 'pdf')을 받아 해당 문서를 LangChain Document 리스트로 로딩
    """
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

    # 임시 파일 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    # 로더 선택
    if file_type == "pptx":
        loader = UnstructuredPowerPointLoader(tmp_path)
    elif file_type == "docx":
        loader = UnstructuredWordDocumentLoader(tmp_path)
    elif file_type == "pdf":
        loader = PyPDFLoader(tmp_path)

    return loader.load()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❗ 사용법: python main.py [pptx|docx|pdf]")
        sys.exit(1)

    file_type = sys.argv[1].lower()

    try:
        docs = load_docs_by_type(file_type)
        print(f"✅ 총 문서 수: {len(docs)}")
        print("📄 미리보기:\n", docs[0])
    except Exception as e:
        print("🚫 오류 발생:", e)
        sys.exit(1)
