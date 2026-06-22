from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def add_document_to_vectorstore(text, filename):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    print("=" * 50)
    print("FILE:", filename)
    print("CHUNKS:", len(chunks))
    print("=" * 50)

    metadatas = [
    {
        "source": filename,
        "document": filename
    }
    for _ in chunks
]

    try:

        vectorstore = FAISS.load_local(
            "vectorstore",
            embeddings,
            allow_dangerous_deserialization=True
        )

        vectorstore.add_texts(
            chunks,
            metadatas=metadatas
        )

    except Exception:

        vectorstore = FAISS.from_texts(
            chunks,
            embedding=embeddings,
            metadatas=metadatas
        )

    vectorstore.save_local("vectorstore")