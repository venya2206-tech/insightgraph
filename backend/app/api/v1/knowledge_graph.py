from fastapi import APIRouter, HTTPException
from app.services.knowledge_graph_service import KnowledgeGraphService
from pydantic import BaseModel
from typing import Optional


class EntityQuery(BaseModel):
    entity_name: str


router = APIRouter()
kg_service = KnowledgeGraphService()


@router.get('/knowledge-graph/stats')
async def get_graph_stats():
    return await kg_service.get_graph_stats()


@router.get('/knowledge-graph/entity/{entity_name}')
async def get_entity_relationships(entity_name: str):
    result = await kg_service.find_entity_relationships(entity_name)
    if not result.get('sources'):
        raise HTTPException(status_code=404, detail='Entity not found')
    return result


@router.get('/knowledge-graph/source/{source_id}/network')
async def get_source_network(source_id: str):
    return await kg_service.get_entity_network(source_id)


@router.get('/knowledge-graph/common/{source_id_1}/{source_id_2}')
async def find_common_entities(source_id_1: str, source_id_2: str):
    return await kg_service.find_common_entities(source_id_1, source_id_2)
