from dotenv import load_dotenv
import os

import google.generativeai as genai
# from google import genai

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)


def ask_question(question):

    docs_with_scores = vectorstore.similarity_search_with_score(
        question,
        k=7
    )

    relevant_docs = []

    for doc, score in docs_with_scores:
        # print("=" * 50)
        # print(score)
        # print(doc.page_content[:200])

        print(f"Score: {score}")

        # Lower score = better match
        if score < 1.5:
            relevant_docs.append(doc)

    if len(relevant_docs) == 0:

        return """
            <h2>Information Not Available</h2>

            <p>
            The provided policy documents do not contain information related to your question.
            </p>

            <p>
            Please ask a question that is relevant to the uploaded company policies.
            </p>
            """

    context = "\n\n".join(
        [doc.page_content for doc in relevant_docs]
    )

    prompt = f"""
        Answer ONLY from the provided context.

        IMPORTANT RULES:

        1. Do not make up information.
        2. If the answer is not in the context, say:
        "Information Not Available"
        3. Use HTML formatting only.
        4. Use headings and bullet points.
        5. Keep answers concise and professional.

        Use only these tags:

        <h2>
        <h3>
        <ul>
        <li>
        <p>
        <b>

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

    try:

        response = model.generate_content(
            prompt
        )

        if not response.candidates:

            return """
                <h2>Information Not Available</h2>

                <p>
                The provided context does not contain enough information to answer this question.
                </p>
                """

        return response.text

    except Exception as e:

        print("Gemini Error:", e)

        return """
        <h2>Information Not Available</h2>

        <p>
        The provided context does not contain enough information to answer this question.
        </p>

        <p>
        Please ask a question related to the uploaded policy documents.
        </p>
        """