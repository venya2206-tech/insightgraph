from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import init_db
from app.api.v1.health import router as health_router
from app.api.v1.research import router as research_router
from app.api.v1.ingestion import router as ingestion_router
from app.api.v1.nlp import router as nlp_router
from app.api.v1.knowledge_graph import router as kg_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.reports import router as reports_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting InsightGraph backend...")
    await init_db()
    yield


app = FastAPI(
    title="InsightGraph API",
    description="AI-Powered Research Report Generator with Knowledge Graphs",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(research_router)
app.include_router(ingestion_router)
app.include_router(nlp_router)
app.include_router(kg_router)
app.include_router(analysis_router)
app.include_router(reports_router)


@app.get("/")
async def root():
    return {"message": "InsightGraph API is running"}