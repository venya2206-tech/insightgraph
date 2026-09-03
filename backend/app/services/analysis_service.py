from typing import List, Dict
from app.core.neo4j_driver import get_neo4j_driver


class AnalysisService:
    def __init__(self):
        pass

    async def calculate_credibility(self, source_id: str) -> Dict:
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                result = await session.run(
                    "MATCH (s:Source {id: $sid})-[:MENTIONS]->(e:Entity) RETURN count(e) as entity_count",
                    sid=str(source_id)
                )
                record = await result.single()
                entity_count = record["entity_count"] if record else 0

                result2 = await session.run(
                    "MATCH (s:Source {id: $sid})-[:CONTAINS]->(c:Claim) RETURN count(c) as claim_count",
                    sid=str(source_id)
                )
                record2 = await result2.single()
                claim_count = record2["claim_count"] if record2 else 0

                result3 = await session.run(
                    "MATCH (s:Source {id: $sid})-[:MENTIONS]->(e:Entity)<-[:MENTIONS]-(s2:Source) WHERE s2.id <> $sid RETURN count(DISTINCT s2) as cross_refs",
                    sid=str(source_id)
                )
                record3 = await result3.single()
                cross_refs = record3["cross_refs"] if record3 else 0

                score = min(1.0, (entity_count * 0.1) + (claim_count * 0.2) + (cross_refs * 0.3))

                return {
                    "source_id": source_id,
                    "credibility_score": round(score, 2),
                    "factors": {
                        "entity_richness": entity_count,
                        "claim_density": claim_count,
                        "cross_references": cross_refs
                    }
                }
        except Exception as e:
            print("Credibility error: " + str(e))
            return {"source_id": source_id, "credibility_score": 0.0, "factors": {}}

    async def get_entity_frequency(self, limit: int = 20) -> List[Dict]:
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                result = await session.run(
                    "MATCH (e:Entity)<-[:MENTIONS]-(s:Source) RETURN e.name as name, e.entity_type as entity_type, count(s) as frequency ORDER BY frequency DESC LIMIT $lim",
                    lim=limit
                )
                return [dict(record) async for record in result]
        except Exception as e:
            print("Entity frequency error: " + str(e))
            return []

    async def get_topic_summary(self) -> List[Dict]:
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                result = await session.run(
                    "MATCH (e:Entity)<-[:MENTIONS]-(s:Source) RETURN e.entity_type as topic, count(DISTINCT s) as source_count, count(e) as mention_count ORDER BY mention_count DESC"
                )
                return [dict(record) async for record in result]
        except Exception as e:
            print("Topic summary error: " + str(e))
            return []

    async def find_source_connections(self, source_id: str) -> List[Dict]:
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                result = await session.run(
                    "MATCH (s:Source {id: $sid})-[:MENTIONS]->(e:Entity)<-[:MENTIONS]-(s2:Source) WHERE s2.id <> $sid RETURN s2.title as connected_source, s2.id as source_id, collect(DISTINCT e.name) as shared_entities",
                    sid=str(source_id)
                )
                return [dict(record) async for record in result]
        except Exception as e:
            print("Source connections error: " + str(e))
            return []

    async def get_research_overview(self) -> Dict:
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                result = await session.run("MATCH (n) RETURN labels(n) as label, count(n) as count")
                nodes = [dict(record) async for record in result]

                result2 = await session.run("MATCH ()-[r]->() RETURN type(r) as type, count(r) as count")
                relationships = [dict(record) async for record in result2]

                result3 = await session.run(
                    "MATCH (e:Entity)<-[:MENTIONS]-(s:Source) RETURN e.name as name, e.entity_type as entity_type, count(s) as frequency ORDER BY frequency DESC LIMIT 10"
                )
                top_entities = [dict(record) async for record in result3]

                return {
                    "total_nodes": nodes,
                    "total_relationships": relationships,
                    "top_entities": top_entities
                }
        except Exception as e:
            print("Research overview error: " + str(e))
            return {"total_nodes": [], "total_relationships": [], "top_entities": []}