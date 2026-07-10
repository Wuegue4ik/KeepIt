from datetime import datetime
from src.database.database import DB_Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy


class NoteTag(DB_Base):
    __tablename__ = "notes_tags"

    note_id: Mapped[int] = mapped_column(sa.ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(sa.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    note: Mapped["Note"] = relationship(back_populates="note_tags")
    tag: Mapped["Tag"] = relationship(back_populates="tag_notes")


class Note(DB_Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    text: Mapped[str | None] = mapped_column(sa.Text)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.now)

    note_tags: Mapped[list["NoteTag"]] = relationship(back_populates="note", cascade="all, delete-orphan")

    @staticmethod
    def create_note_tag_by_tag(tag_obj: "Tag") -> "NoteTag":
        return NoteTag(tag=tag_obj)

    tags: AssociationProxy[list["Tag"]] = association_proxy(
        target_collection="note_tags",
        attr="tag",
        creator=create_note_tag_by_tag
    )


class Tag(DB_Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(50), unique=True)

    tag_notes: Mapped[list["NoteTag"]] = relationship(back_populates="tag", cascade="all, delete-orphan")

    @staticmethod
    def create_note_tag_by_note(note_obj: "Note") -> "NoteTag":
        return NoteTag(note=note_obj)
    
    notes: AssociationProxy[list["Note"]] = association_proxy(
        target_collection="tag_notes", 
        attr="note",
        creator=create_note_tag_by_note
    )