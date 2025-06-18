from langchain.text_splitter import Language, CodeTextSplitter

code = """
import os

def foo():
    print("Hello")

class MyClass:
    def method(self):
        print("method called")

if __name__ == "__main__":
    foo()
"""

# PythonCodeTextSplitter 생성

splitter = CodeTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_lines=10,
    chunk_overlap_lines=2
)

# split_text() 메서드로 분할
chunks = splitter.split_text(code)

# 또는 create_documents()로 LangChain 문서 객체 생성
docs = splitter.create_documents([code])

# 결과 출력
for i, doc in enumerate(docs):
    print(f"--- Chunk {i+1} ---")
    print(doc.page_content)
