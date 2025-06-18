from langchain_text_splitters import CharacterTextSplitter

# 예시 원본문자열
text = (
    "1. 첫 번째 문단입니다.\n"
    "이 문단은 설명을 포함합니다.\n\n"
    "2. 두 번째 문단입니다.\n"
    "여기에는 추가 정보가 포함되어 있습니다.\n\n"
    "3. 세 번째 문단입니다.\n"
    "이것은 테스트용 문장입니다.\n\n"
    "4. 네 번째 문단입니다.\n"
    "마지막 문장입니다."
)

# 분할기 설정
splitter = CharacterTextSplitter(
    separator="\n",             # 줄바꿈 기준 분할
    chunk_size=50,             # 각 청크 최대 100자
    chunk_overlap=20,           # 20자 겹치게
    length_function=len
)

# 분할 수행
chunks = splitter.split_text(text)

# 결과 출력
print("총 청크 개수:", len(chunks))
for i, chunk in enumerate(chunks):
    print(f"\n== Chunk {i+1} ==\n{chunk}")
