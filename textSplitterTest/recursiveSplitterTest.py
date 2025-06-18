from langchain_text_splitters import RecursiveCharacterTextSplitter

# 예시 원본 텍스트
text = (
    "제1장. 서론\n\n"
    "이 문서는 테스트용 텍스트입니다. 줄바꿈도 있고, 공백도 있습니다.\n"
    "내용이 계속 이어집니다.\n\n"
    "제2장. 본론\n\n"
    "여기에는 좀 더 긴 설명이 포함되어 있습니다. 여러 문장이 포함됩니다. "
    "길이가 길면 재귀적으로 더 잘게 나눌 것입니다."
)

# RecursiveCharacterTextSplitter 인스턴스 생성
splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=0,
    separators=["\n\n", "\n", " ", ""],  # 문단 → 줄 → 단어 → 문자 순
    is_separator_regex=False
)

# 텍스트 분할
chunks = splitter.split_text(text)

# 결과 출력
print(f"총 청크 수: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ---\n{chunk}")
