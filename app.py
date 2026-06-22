from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from chatbot import ask_question

from database import SessionLocal
from models import Conversation
from models import Message

from fastapi import UploadFile
from fastapi import File

import shutil

from services.pdf_service import extract_pdf_text
from services.vector_service import add_document_to_vectorstore

from models import UploadedPDF
import os


app = FastAPI()

# Static Files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# Templates
templates = Jinja2Templates(
    directory="templates"
)

class QueryRequest(BaseModel):
    conversation_id: int
    question: str


# @app.get("/")
# def home(request: Request):

#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request
#         }
#     )

@app.get("/")
def home(request: Request):

    print("INDEX ROUTE HIT")

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )




@app.get("/conversations")
def get_conversations():

    db = SessionLocal()

    conversations = db.query(
        Conversation
    ).order_by(
        Conversation.id.desc()
    ).all()

    db.close()

    return [
        {
            "id": c.id,
            "title": c.title
        }
        for c in conversations
    ]

@app.post("/conversation")
def create_conversation():

    db = SessionLocal()

    conversation = Conversation(
        title="New Chat"
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    db.close()

    return {
        "conversation_id": conversation.id
    }

@app.get("/conversation/{conversation_id}")
def get_messages(
    conversation_id: int
):

    db = SessionLocal()

    messages = db.query(
        Message
    ).filter(
        Message.conversation_id == conversation_id
    ).all()

    db.close()

    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content
        }
        for m in messages
    ]

@app.delete(
    "/conversation/{conversation_id}"
)
def delete_conversation(
    conversation_id: int
):

    db = SessionLocal()

    db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).delete()

    db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).delete()

    db.commit()

    db.close()

    return {
        "message":"deleted"
    }

@app.delete("/conversations")
def delete_all_conversations():

    db = SessionLocal()

    db.query(Message).delete()

    db.query(Conversation).delete()

    db.commit()

    db.close()

    return {
        "message": "All conversations deleted"
    }

@app.post("/ask")
def ask(req: QueryRequest):

    db = SessionLocal()

    try:

        user_message = Message(
            conversation_id=req.conversation_id,
            role="user",
            content=req.question
        )

        db.add(user_message)
        db.commit()

        conversation = db.query(
            Conversation
        ).filter(
            Conversation.id == req.conversation_id
        ).first()

        if conversation and conversation.title == "New Chat":
            conversation.title = req.question[:50]
            db.commit()

        answer = ask_question(
            req.question
        )

        assistant_message = Message(
            conversation_id=req.conversation_id,
            role="assistant",
            content=answer
        )

        db.add(assistant_message)
        db.commit()

        return {
            "answer": answer
        }

    finally:
        db.close()


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    db = SessionLocal()

    import os

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    existing = db.query(
        UploadedPDF
    ).filter(
        UploadedPDF.filename == file.filename
    ).first()

    if existing:

        db.close()

        return {
            "message": "PDF already uploaded"
        }

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Extract text
    text = extract_pdf_text(
        file_path
    )

    # print("=" * 50)
    # print("FILE:", file.filename)
    # print("TEXT LENGTH:", len(text))
    # print(text[:1000])
    # print("=" * 50)

    # Add to vector store
    add_document_to_vectorstore(
        text,
        file.filename
    )

    pdf_record = UploadedPDF(
    filename=file.filename
    )

    db.add(pdf_record)
    db.commit()
    db.close()

    return {
        "message": f"{file.filename} uploaded successfully"
    }

@app.get("/pdfs")
def get_pdfs():

    db = SessionLocal()

    pdfs = db.query(
        UploadedPDF
    ).all()

    db.close()

    return [
        {
            "id": pdf.id,
            "filename": pdf.filename
        }
        for pdf in pdfs
    ]

@app.delete("/pdf/{pdf_id}")
def delete_pdf(pdf_id:int):

    db = SessionLocal()

    pdf = db.query(
        UploadedPDF
    ).filter(
        UploadedPDF.id == pdf_id
    ).first()

    if not pdf:

        db.close()

        return {
            "message":"PDF not found"
        }

    db.delete(pdf)

    db.commit()

    db.close()

    return {
        "message":"PDF deleted"
    }

# if __name__ == "__main__":
#     import webbrowser
#     webbrowser.open("http://127.0.0.1:8000")