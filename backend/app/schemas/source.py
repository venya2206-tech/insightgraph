from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class SourceCreate(BaseModel):
    source_type: str
    input: str
    url: Optional[str] = None


class SourceResponse(BaseModel):
    id: UUID
    research_id: UUID
    source_type: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    raw_text: Optional[str] = None
    credibility_score: Optional[float] = None
    processed: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
