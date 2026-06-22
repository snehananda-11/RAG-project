from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import declarative_base

from datetime import datetime

Base = declarative_base()


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id")
    )

    role = Column(
        String(20)
    )

    content = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class UploadedPDF(Base):

    __tablename__ = "uploaded_pdfs"

    id = Column(
        Integer,
        primary_key=True
    )

    filename = Column(
        String,
        unique=True
    )