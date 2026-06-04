from fastapi import APIRouter, Depends, HTTPException

from src.database import schemas
from src.database.schemas import Note as Pydantic_Note
from src.database.models import Note as DB_Note, Tag as DB_Tag
from src.database.database import get_db

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/db")

@router.get("/notes", response_model=list[Pydantic_Note])
async def get_notes_db(db: AsyncSession = Depends(get_db)):
    query = select(DB_Note).options(selectinload(DB_Note.tags))
    result = await db.execute(query)

    notes = result.scalars().all()

    return notes

@router.get("/notes/{note_id}", response_model=Pydantic_Note)
async def view_note_db(note_id: int, db: AsyncSession = Depends(get_db)):
    query = select(DB_Note).options(selectinload(DB_Note.tags)).where(DB_Note.id==note_id)
    result = await db.execute(query)

    note = result.scalars().first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return note

@router.post("/notes", response_model=Pydantic_Note)
async def add_note_db(note_data: schemas.NoteOnCreate, db: AsyncSession = Depends(get_db)):
    new_note = DB_Note(header=note_data.header, text=note_data.text)

    if note_data.tags:
        tags = list(set(note_data.tags))

        query = select(DB_Tag).where(DB_Tag.name.in_(tags))
        result = await db.execute(query)

        existing_tags = {tag.name: tag for tag in result.scalars().all()}
        final_tags = []

        for tag in tags:
            if tag in existing_tags:
                final_tags.append(existing_tags[tag])
            else:
                new_tag = DB_Tag(name=tag)
                final_tags.append(new_tag)

        new_note.tags = final_tags

    db.add(new_note)
    await db.commit()

    await db.refresh(new_note, attribute_names=["tags"])

    return new_note
