from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    from app.core.database import get_db
    from app.core.neo4j_driver import test_neo4j_connection
    from app.core.redis_client import test_redis_connection

    services = {}

    try:
        async for db in get_db():
            await db.execute("SELECT 1")
            services["postgres"] = "connected"
            break
    except Exception:
        services["postgres"] = "disconnected"

    services["neo4j"] = "connected" if await test_neo4j_connection() else "disconnected"
    services["redis"] = "connected" if await test_redis_connection() else "disconnected"

    status = "healthy" if all(v == "connected" for v in services.values()) else "degraded"

    return {
        "status": status,
        "version": "0.1.0",
        "services": services
    }
