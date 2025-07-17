from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users, topics, learning_paths, lessons, videos, voices

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(learning_paths.router, prefix="/learning-paths", tags=["learning-paths"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
api_router.include_router(voices.router, prefix="/voices", tags=["voices"])

