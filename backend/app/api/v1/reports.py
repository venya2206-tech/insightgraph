from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.report_service import ReportService

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])
service = ReportService()


class ReportRequest(BaseModel):
    research_id: Optional[str] = None


class EntityReportRequest(BaseModel):
    entity_name: str


@router.post("/generate")
async def generate_report(request: ReportRequest):
    result = await service.generate_report(request.research_id)
    return result


@router.post("/entity")
async def generate_entity_report(request: EntityReportRequest):
    result = await service.get_entity_report(request.entity_name)
    if not result:
        raise HTTPException(status_code=404, detail="Entity not found")
    return result