import os
import fitz

from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_FOLDER = "data"

documents = []

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

for filename in os.listdir(DATA_FOLDER):

    if filename.endswith(".pdf"):

        pdf_path = os.path.join(DATA_FOLDER, filename)

        print(f"Processing: {filename}")

        pdf = fitz.open(pdf_path)

        for page_num, page in enumerate(pdf):

            text = page.get_text()

            chunks = splitter.split_text(text)

            for chunk in chunks:

                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "source": filename,
                            "page": page_num + 1
                        }
                    )
                )

print(f"\nTotal Chunks: {len(documents)}")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(
    documents,
    embeddings
)

vectorstore.save_local("vectorstore")

print("Multi-PDF FAISS Index Created!")




# print(len(vector))

# print("Total Chucks: ", len(chunks))
# print(chunks[0])


# # for page_num, page in enumerate(doc):
# #     text += page.get_text()

# # print(text[:1000])
