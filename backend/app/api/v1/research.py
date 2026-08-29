from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.research import ResearchProject
from uuid import UUID, uuid4
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ResearchCreate(BaseModel):
    topic: str
    description: Optional[str] = None


class ResearchResponse(BaseModel):
    id: UUID
    topic: str
    description: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


router = APIRouter()


@router.post('/research', response_model=ResearchResponse)
async def create_research(data: ResearchCreate, db: AsyncSession = Depends(get_db)):
    research = ResearchProject(
        id=uuid4(),
        topic=data.topic,
        description=data.description,
        status='active'
    )
    db.add(research)
    await db.commit()
    await db.refresh(research)
    return research


@router.get('/research', response_model=list[ResearchResponse])
async def list_research(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ResearchProject))
    return result.scalars().all()


@router.get('/research/{research_id}', response_model=ResearchResponse)
async def get_research(research_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ResearchProject).where(ResearchProject.id == research_id)
    )
    research = result.scalar_one_or_none()
    if not research:
        raise HTTPException(status_code=404, detail='Research project not found')
    return research
