from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Enterprise HR knowledge base
docs = [
    Document(page_content="Employees are allowed 12 casual leaves per year."),
    Document(page_content="Employees are allowed 10 sick leaves per year."),
    Document(page_content="Sick leave requires medical proof if the leave duration is more than 2 days."),
    Document(page_content="Leaves must be approved by the reporting manager before they are confirmed."),
    Document(page_content="Earned leave can be carried forward up to 30 days."),
    Document(page_content="Employees should apply for planned leave at least 3 working days in advance."),
    Document(page_content="Emergency leave can be applied on the same day, but manager approval is still required."),
    Document(page_content="Emergency leave can be applied on the same day, but manager approval is still required."),
    Document(page_content="Employees can work remotely up to 2 days per week with manager approval."),
    Document(page_content="Emergency leave requests are reviewed by HR and managers based on business requirements."),
    Document(page_content="New employees receive laptop credentials, email access, and security training during onboarding."),

    # Onboarding knowledge
    Document(page_content="New employees must complete onboarding by submitting ID proof, bank details, joining forms, laptop request, and emergency contact details."),
    Document(page_content="Onboarding checklist includes HR documentation, manager introduction, system access setup, email account activation, and compliance training."),
    Document(page_content="New joiners must attend orientation training and complete mandatory security awareness training within the first week."),

    # Compliance knowledge
    Document(page_content="HR actions must follow compliance rules related to approval, documentation, employee eligibility, and audit tracking."),
    Document(page_content="The Compliance Decision Agent checks whether employee requests satisfy HR policy before suggesting the next action."),
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
    results = db.similarity_search(query, k=1)
    return results[0].page_content if results else "No policy found."


# Test
if __name__ == "__main__":
    while True:
        q = input("Ask HR Policy: ")
        print(get_policy_answer(q))
        print("-" * 50)