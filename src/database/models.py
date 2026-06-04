from datetime import datetime
from src.database.database import DB_Base
from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship

notes_tags = Table(
    "notes_tags",
    DB_Base.metadata,
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)


class Note(DB_Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    header = Column(String(50), nullable=False)
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    tags = relationship("Tag", secondary=notes_tags, back_populates="notes")


class Tag(DB_Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    notes = relationship("Note", secondary=notes_tags, back_populates="tags")