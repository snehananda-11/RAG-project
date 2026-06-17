from fastapi import FastAPI
from pydantic import BaseModel

from chatbot import ask_question

app = FastAPI(
    title="Company Policy Chatbot",
    version="1.0"
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "message": "Company Policy Chatbot API Running"
    }

# @app.post("/ask")
# def ask(req: QueryRequest):

#     answer = ask_question(req.question)

#     return {
#         "question": req.question,
#         "answer": answer
#     }


@app.post("/ask")
def ask(req: QueryRequest):

    return ask_question(req.question)

if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:8000/docs")