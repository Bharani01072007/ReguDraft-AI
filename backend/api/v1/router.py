from fastapi import APIRouter
from backend.api.v1.endpoints import auth, projects, documents, history, knowledge, exports, audit

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents & Generation"])
api_router.include_router(history.router, prefix="/history", tags=["Document History"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge Search & RAG"])
api_router.include_router(exports.router, prefix="/exports", tags=["Exports & Templates"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit Trails"])
