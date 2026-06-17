from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from chatbot import ask_question

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


@app.post("/ask")
def ask(req: QueryRequest):

    answer = ask_question(
        req.question
    )

    return {
        "answer": answer
    }


# if __name__ == "__main__":
#     import webbrowser
#     webbrowser.open("http://127.0.0.1:8000")