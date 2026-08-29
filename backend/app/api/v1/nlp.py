from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.source import Chunk
from app.models.entity import Entity
from app.models.claim import Claim
from app.services.nlp_service import NLPService
from uuid import UUID

router = APIRouter()
nlp_service = NLPService()


@router.get('/nlp/chunk/{chunk_id}/entities')
async def get_chunk_entities(chunk_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Entity).where(Entity.chunk_id == chunk_id)
    )
    return result.scalars().all()


@router.get('/nlp/chunk/{chunk_id}/claims')
async def get_chunk_claims(chunk_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Claim).where(Claim.chunk_id == chunk_id)
    )
    return result.scalars().all()


@router.post('/nlp/process/{chunk_id}')
async def process_chunk_nlp(chunk_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Chunk).where(Chunk.id == chunk_id))
    chunk = result.scalar_one_or_none()

    if not chunk:
        raise HTTPException(status_code=404, detail='Chunk not found')

    nlp_results = nlp_service.process_chunk(chunk.text)

    for ent_data in nlp_results['entities']:
        entity = Entity(
            chunk_id=chunk.id,
            name=ent_data['name'],
            entity_type=ent_data['entity_type'],
            confidence=ent_data['confidence']
        )
        db.add(entity)

    for claim_data in nlp_results['claims']:
        claim = Claim(
            chunk_id=chunk.id,
            claim_text=claim_data['claim_text'],
            claim_type=claim_data['claim_type'],
            confidence=claim_data['confidence']
        )
        db.add(claim)

    await db.commit()

    return {
        'chunk_id': str(chunk.id),
        'entities_found': len(nlp_results['entities']),
        'claims_found': len(nlp_results['claims']),
        'statistics_found': len(nlp_results['statistics']),
        'word_count': nlp_results['word_count']
    }
