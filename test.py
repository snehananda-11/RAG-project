# import fitz

# from langchain_text_splitters import RecursiveCharacterTextSplitter

# print("Everything works!")

from chatbot import ask_question

question = "What is the hiring policy?"

answer = ask_question(question)

print(answer)
