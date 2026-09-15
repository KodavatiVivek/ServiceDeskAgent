from fastapi import FastAPI
from app.api.routes import router as orchestrator_router
from app.api.health import router as health_router

app = FastAPI(title="Orchestrator Service", version="0.1.0")

app.include_router(health_router)
app.include_router(orchestrator_router)
