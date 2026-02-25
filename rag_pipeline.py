"""
This script will help to run the RAG based LLM independently for testing purpose.
We must use 'rag_engine.py' module that can be called from within the Flask app as and when required.
"""

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI


# ======================================================
# 1️⃣ LOAD ENV VARIABLES
# ======================================================
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env file")


# ======================================================
# 2️⃣ LOAD KNOWLEDGE BASE
# ======================================================
loader = TextLoader("hospital_knowledge_base.txt", encoding="utf-8")
documents = loader.load()

print("Knowledge base loaded.")


# ======================================================
# 3️⃣ CHUNKING
# ======================================================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = splitter.split_documents(documents)

print(f"Total chunks created: {len(chunks)}")


# ======================================================
# 4️⃣ EMBEDDING MODEL
# ======================================================
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ======================================================
# 5️⃣ BUILD OR LOAD FAISS INDEX
# ======================================================
if os.path.exists("faiss_index"):
    print("Loading existing FAISS index...")
    vectorstore = FAISS.load_local(
        "faiss_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )
else:
    print("Creating new FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local("faiss_index")


retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


# ======================================================
# 6️⃣ LLM
# ======================================================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)


# ======================================================
# 7️⃣ SIMPLE TEST QUERY LOOP
# ======================================================

while True:
    query = input("\nAsk a question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    # Retrieve relevant documents
    docs = retriever.invoke (query)

    context = "\n\n".join([doc.page_content for doc in docs])

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

    print("\nAnswer:")
    print(response.content)