from typing import List, Dict
from app.core.neo4j_driver import get_neo4j_driver


class KnowledgeGraphService:
    def __init__(self):
        pass

    async def add_source(self, source_id: str, title: str, source_type: str):
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                q = "MERGE (s:Source {id: $sid}) SET s.title = $t, s.source_type = $st"
                await session.run(q, sid=str(source_id), t=str(title), st=str(source_type))
                print("Neo4j: Added source " + str(source_id))
        except Exception as e:
            print("Neo4j add_source error: " + str(e))

    async def add_entity(self, name: str, entity_type: str, chunk_id: str, source_id: str):
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                q1 = "MERGE (e:Entity {name: $nm}) SET e.entity_type = $et"
                await session.run(q1, nm=str(name), et=str(entity_type))
                q2 = "MATCH (s:Source {id: $sid}), (e:Entity {name: $nm}) MERGE (s)-[:MENTIONS]->(e)"
                await session.run(q2, sid=str(source_id), nm=str(name))
                print("Neo4j: Added entity " + str(name))
        except Exception as e:
            print("Neo4j add_entity error: " + str(e))

    async def add_claim(self, claim_text: str, claim_type: str, source_id: str):
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                q1 = "MERGE (c:Claim {text: $ct}) SET c.claim_type = $cpty"
                await session.run(q1, ct=str(claim_text), cpty=str(claim_type))
                q2 = "MATCH (s:Source {id: $sid}), (c:Claim {text: $ct}) MERGE (s)-[:CONTAINS]->(c)"
                await session.run(q2, sid=str(source_id), ct=str(claim_text))
                print("Neo4j: Added claim")
        except Exception as e:
            print("Neo4j add_claim error: " + str(e))

    async def find_entity_relationships(self, entity_name: str) -> Dict:
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                result = await session.run(
                    "MATCH (e:Entity {name: $nm})<-[:MENTIONS]-(s:Source) RETURN s.title as source_title, s.source_type as source_type",
                    nm=str(entity_name)
                )
                sources = [dict(record) async for record in result]

                result2 = await session.run(
                    "MATCH (e:Entity {name: $nm})<-[:MENTIONS]-(s:Source)-[:MENTIONS]->(e2:Entity) WHERE e2.name <> $nm RETURN DISTINCT e2.name as related_entity, e2.entity_type as entity_type LIMIT 10",
                    nm=str(entity_name)
                )
                related = [dict(record) async for record in result2]

                return {"entity": entity_name, "sources": sources, "related_entities": related}
        except Exception as e:
            print("Neo4j find_entity error: " + str(e))
            return {"entity": entity_name, "sources": [], "related_entities": []}

    async def get_entity_network(self, source_id: str) -> List[Dict]:
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                result = await session.run(
                    "MATCH (s:Source {id: $sid})-[:MENTIONS]->(e:Entity) RETURN e.name as name, e.entity_type as entity_type",
                    sid=str(source_id)
                )
                return [dict(record) async for record in result]
        except Exception as e:
            print("Neo4j get_network error: " + str(e))
            return []

    async def find_common_entities(self, source_id_1: str, source_id_2: str) -> List[Dict]:
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                result = await session.run(
                    "MATCH (s1:Source {id: $id1})-[:MENTIONS]->(e:Entity)<-[:MENTIONS]-(s2:Source {id: $id2}) RETURN e.name as name, e.entity_type as entity_type",
                    id1=str(source_id_1), id2=str(source_id_2)
                )
                return [dict(record) async for record in result]
        except Exception as e:
            print("Neo4j find_common error: " + str(e))
            return []

    async def get_graph_stats(self) -> Dict:
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                result = await session.run("MATCH (n) RETURN labels(n) as label, count(n) as count")
                nodes = [dict(record) async for record in result]

                result2 = await session.run("MATCH ()-[r]->() RETURN type(r) as type, count(r) as count")
                relationships = [dict(record) async for record in result2]

                return {"nodes": nodes, "relationships": relationships}
        except Exception as e:
            print("Neo4j stats error: " + str(e))
            return {"nodes": [], "relationships": []}
