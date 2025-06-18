from langchain_text_splitters import HTMLHeaderTextSplitter

headers_to_split_on = [("h1", "Main Topic"), ("h2", "Sub Topic")]

splitter = HTMLHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    return_each_element=False
)

html_content = """
<html>
  <body>
    <h1>Introduction</h1>
    <p>Welcome to the introduction section.</p>
    <h2>Background</h2>
    <p>Some background details here.</p>
    <h1>Conclusion</h1>
    <p>Final thoughts.</p>
  </body>
</html>
"""

documents = splitter.split_text(html_content)

for document in documents:
    for line in str(document).splitlines():
        print(line)
    print()  


# 'documents' now contains Document objects reflecting the hierarchy:
# - Document with metadata={"Main Topic": "Introduction"} and
#   content="Introduction"
# - Document with metadata={"Main Topic": "Introduction"} and
#   content="Welcome to the introduction section."
# - Document with metadata={"Main Topic": "Introduction",
#   "Sub Topic": "Background"} and content="Background"
# - Document with metadata={"Main Topic": "Introduction",
#   "Sub Topic": "Background"} and content="Some background details here."
# - Document with metadata={"Main Topic": "Conclusion"} and
#   content="Conclusion"
# - Document with metadata={"Main Topic": "Conclusion"} and
#   content="Final thoughts."