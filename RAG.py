from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
# 👉 Create HR policy manually
docs = [
    Document(page_content="Employees are allowed 12 casual leaves per year."),
    Document(page_content="Sick leave requires medical proof for more than 2 days."),
    Document(page_content="Leaves must be approved by the manager."),
    Document(page_content="Earned leave can be carried forward up to 30 days."),
]

# Split text
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Vector DB
db = FAISS.from_documents(chunks, embeddings)

# Query function
def get_policy_answer(query: str):
    results = db.similarity_search(query, k=2)
    return "\n".join([r.page_content for r in results])


# 👉 Test
if __name__ == "__main__":
    while True:
        q = input("Ask HR Policy: ")
        print(get_policy_answer(q))
        print("-" * 50)