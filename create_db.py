from database import engine
from models import Base, Conversation, Message, UploadedPDF

Base.metadata.create_all(bind=engine)

print("Database Created!")