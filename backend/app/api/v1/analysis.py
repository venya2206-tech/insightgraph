from fastapi import APIRouter, HTTPException
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])
service = AnalysisService()


@router.get("/credibility/{source_id}")
async def get_credibility(source_id: str):
    result = await service.calculate_credibility(source_id)
    if not result:
        raise HTTPException(status_code=404, detail="Source not found")
    return result


@router.get("/entities/frequency")
async def get_entity_frequency(limit: int = 20):
    return await service.get_entity_frequency(limit)


@router.get("/topics")
async def get_topics():
    return await service.get_topic_summary()


@router.get("/connections/{source_id}")
async def get_connections(source_id: str):
    return await service.find_source_connections(source_id)


@router.get("/overview")
async def get_overview():
    return await service.get_research_overview()