import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI


# ======================================================
# 1️⃣ LOAD ENV
# ======================================================
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env")


# ======================================================
# 2️⃣ BUILD OR LOAD VECTOR STORE
# ======================================================

def load_vectorstore():
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists("faiss_index"):
        return FAISS.load_local(
            "faiss_index",
            embedding_model,
            allow_dangerous_deserialization=True
        )

    loader = TextLoader("hospital_knowledge_base.txt", encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local("faiss_index")

    return vectorstore


vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ======================================================
# 3️⃣ LLM
# ======================================================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)

# ======================================================
# 4️⃣ SIMPLE RAG FUNCTION (MANUAL)
# ======================================================

def ask_question(query: str):

    # Retrieve relevant documents
    docs = retriever.invoke (query)

    # Combine context
    context = "\n\n".join([doc.page_content for doc in docs])

    # Build prompt manually
    prompt = f"""
You are a hospital assistant for MediSync Hospital.

Answer ONLY using the context below.
If the answer is not found in the context, say you do not have that information.

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content