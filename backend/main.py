import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.api.v1.router import api_router
from backend.database.session import engine
from backend.database.models import Base

# Create tables automatically on startup (SQLite fallback or Postgres)
# In production, migrations (Alembic) are preferred, but this guarantees 
# immediate out-of-the-box execution for validation.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API and Multi-Agent RAG Orchestration Layer for Regulatory Intelligence",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set CORS middleware parameters to allow access from local frontend servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adapt to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bind the v1 endpoints router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve files locally to simulate object storage bucket access
storage_dir = os.path.join(os.path.dirname(__file__), "storage_temp")
os.makedirs(storage_dir, exist_ok=True)
app.mount("/static/storage", StaticFiles(directory=storage_dir), name="storage")

@app.get("/", tags=["Status"])
def read_root():
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database_connected": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
