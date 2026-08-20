import json
import redis.asyncio as aioredis

from typing import AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import PaginatedNotesResponse, Note as Pydantic_Note, NoteOnCreate
from src.database.models import Note as DB_Note, Tag as DB_Tag, NoteTag as DB_NoteTag
from src.database.database import get_db

def note_redis_key(key: int) -> str:
    return f"notes:{key}"

async def get_redis(request: Request) -> AsyncGenerator[aioredis.Redis, None]:
    yield request.app.state.redis

router = APIRouter()

async def update_note_tags(note: DB_Note, new_tag_names: list[str] | None, db: AsyncSession):
    if not new_tag_names:
        note.tags = []
        return

    unique_names = list(set(new_tag_names))
    
    query = select(DB_Tag).where(DB_Tag.name.in_(unique_names))
    result = await db.execute(query)
    existing_tags = {tag.name: tag for tag in result.scalars().all()}
    
    final_tags: list[DB_Tag] = []
    for name in unique_names:
        if name in existing_tags:
            final_tags.append(existing_tags[name])
        else:
            final_tags.append(DB_Tag(name=name))
            
    note.tags.clear()
    note.tags.extend(final_tags)

@router.get("/notes", response_model=PaginatedNotesResponse)
async def get_notes(
        page: int = Query(1, ge=1, description="Page number (starts with 1)"),
        size: int = Query(20, ge=1, le=100, description="Number of items per page"),
        db: AsyncSession = Depends(get_db)
    ):
    offset: int = (page - 1) * size

    count_query = select(func.count()).select_from(DB_Note)
    total = (await db.execute(count_query)).scalar_one()

    query = (
        select(DB_Note)
        .options(selectinload(DB_Note.note_tags).selectinload(DB_NoteTag.tag))
        .order_by(DB_Note.created_at.desc())
        .offset(offset)
        .limit(size)
    )

    result = await db.execute(query)
    notes = result.scalars().unique().all()

    pages = (total + size - 1) // size if total > 0 else 0

    return PaginatedNotesResponse(
        items=notes, total=total, page=page, size=size, pages=pages # type: ignore
    )

@router.get("/notes/{note_id}", response_model=Pydantic_Note)
async def view_note(
        note_id: int,
        db: AsyncSession = Depends(get_db),
        redis: aioredis.Redis = Depends(get_redis)
    ):
    cache_key = note_redis_key(note_id)
    cached_note = await redis.get(cache_key)
    if cached_note:
        return json.loads(cached_note)

    query = select(DB_Note).options(
        selectinload(DB_Note.note_tags).selectinload(DB_NoteTag.tag)
    ).where(DB_Note.id == note_id)

    result = await db.execute(query)
    note = result.scalars().first()
    
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    validate_note = Pydantic_Note.model_validate(note)
    await redis.set(
        cache_key,
        validate_note.model_dump_json(),
        ex=1800
    )
    return note

@router.post("/notes", response_model=Pydantic_Note, status_code=status.HTTP_201_CREATED)
async def add_note(
        note_data: NoteOnCreate,
        db: AsyncSession = Depends(get_db)
    ):
    new_note = DB_Note(header=note_data.header, text=note_data.text)
    
    if note_data.tags:
        await update_note_tags(new_note, note_data.tags, db)
        
    db.add(new_note)
    await db.commit()

    query = select(DB_Note).options(
        selectinload(DB_Note.note_tags).selectinload(DB_NoteTag.tag)
    ).where(DB_Note.id == new_note.id)
    
    result = await db.execute(query)
    return result.scalars().first()

@router.put("/notes/{note_id}", response_model=Pydantic_Note)
async def edit_note(
        note_id: int,
        note_data: NoteOnCreate,
        db: AsyncSession = Depends(get_db),
        redis: aioredis.Redis = Depends(get_redis)
    ):
    query = select(DB_Note).options(
        selectinload(DB_Note.note_tags).selectinload(DB_NoteTag.tag)
    ).where(DB_Note.id == note_id)
    result = await db.execute(query)
    note = result.scalars().first()

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found!")
    
    note.header = note_data.header
    note.text = note_data.text

    current_tag_names = {t.name for t in note.tags}
    incoming_tag_names: set[str] = set(note_data.tags or [])

    if current_tag_names != incoming_tag_names:
        await update_note_tags(note, note_data.tags, db)

    await db.commit()
    await db.refresh(note, attribute_names=["note_tags"])

    await redis.delete(note_redis_key(note_id))

    return note

@router.delete("/notes/{note_id}")
async def delete_note(
        note_id: int,
        db: AsyncSession = Depends(get_db),
        redis: aioredis.Redis = Depends(get_redis)
    ):
    query = select(DB_Note).where(DB_Note.id == note_id)
    result = await db.execute(query)
    note = result.scalars().first()

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found!")
    
    await db.delete(note)
    await db.commit()

    await redis.delete(note_redis_key(note_id))

    return {"message": "Note deleted successfully!"}