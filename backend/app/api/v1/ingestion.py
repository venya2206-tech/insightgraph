from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.source import SourceCreate, SourceResponse
from app.services.ingestion_service import IngestionService
from uuid import UUID

router = APIRouter()

@router.post("/ingestion/research/{research_id}/sources", response_model=SourceResponse)
async def add_source(
    research_id: UUID,
    source: SourceCreate,
    db: AsyncSession = Depends(get_db),
):
    service = IngestionService(db)
    result = await service.ingest_source(research_id, source)
    return result

@router.get("/ingestion/research/{research_id}/sources", response_model=list[SourceResponse])
async def list_sources(
    research_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select
    from app.models.source import Source
    result = await db.execute(
        select(Source).where(Source.research_id == research_id)
    )
    return result.scalars().all()
