from neo4j import AsyncGraphDatabase
from app.core.config import get_settings

settings = get_settings()
_driver = None

async def get_neo4j_driver():
    global _driver
    if _driver is None:
        _driver = AsyncGraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
    return _driver

async def close_neo4j_driver():
    global _driver
    if _driver:
        await _driver.close()
        _driver = None

async def test_neo4j_connection() -> bool:
    try:
        driver = await get_neo4j_driver()
        async with driver.session() as session:
            result = await session.run("RETURN 1 AS num")
            record = await result.single()
            return record["num"] == 1
    except Exception:
        return False
