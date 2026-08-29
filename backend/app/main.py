from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import init_db, engine
from app.core.neo4j_driver import close_neo4j_driver
from app.core.redis_client import close_redis
from app.api.v1.health import router as health_router
from app.api.v1.ingestion import router as ingestion_router
from app.api.v1.nlp import router as nlp_router
from app.api.v1.research import router as research_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Starting InsightGraph backend...')
    await init_db()
    print('Database tables created.')
    yield
    print('Shutting down...')
    await close_neo4j_driver()
    await close_redis()
    await engine.dispose()


app = FastAPI(
    title='InsightGraph API',
    description='Automated Research Report Generator with Multi-Source Synthesis',
    version='0.1.0',
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://127.0.0.1:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health_router, prefix='/api/v1')
app.include_router(ingestion_router, prefix='/api/v1')
app.include_router(nlp_router, prefix='/api/v1')
app.include_router(research_router, prefix='/api/v1')


@app.get('/')
async def root():
    return {'name': 'InsightGraph API', 'version': '0.1.0', 'docs': '/docs'}
