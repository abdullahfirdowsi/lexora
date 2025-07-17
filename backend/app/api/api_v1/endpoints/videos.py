from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File, Form
from sqlalchemy.orm import Session
import os
import uuid

from app.core.deps import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.models.topic import Topic
from app.models.learning_path import LearningPath
from app.models.lesson import Lesson
from app.models.video import Video
from app.services.video_service import video_service
from app.core.config import settings

router = APIRouter()

async def generate_video_task(video_id: int, lesson_text: str, voice_id: str, avatar_path: str):
    """Background task for video generation"""
    from app.db.database import SessionLocal
    
    db = SessionLocal()
    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            return
        
        # Generate unique filenames
        audio_filename = f"{uuid.uuid4()}.mp3"
        video_filename = f"{uuid.uuid4()}.mp4"
        
        audio_path = os.path.join(settings.UPLOAD_DIR, "audio", audio_filename)
        video_path = os.path.join(settings.UPLOAD_DIR, "videos", video_filename)
        
        # Generate video
        result = await video_service.generate_video_from_lesson(
            lesson_text=lesson_text,
            voice_id=voice_id,
            avatar_image_path=avatar_path,
            output_video_path=video_path,
            output_audio_path=audio_path
        )
        
        if result["success"]:
            video.video_url = f"/uploads/videos/{video_filename}"
            video.audio_url = f"/uploads/audio/{audio_filename}"
            video.status = "completed"
        else:
            video.status = "failed"
        
        db.add(video)
        db.commit()
        
    except Exception as e:
        print(f"Video generation task failed: {e}")
        video = db.query(Video).filter(Video.id == video_id).first()
        if video:
            video.status = "failed"
            db.add(video)
            db.commit()
    finally:
        db.close()

@router.post("/generate", response_model=dict)
async def generate_video(
    lesson_id: int = Form(...),
    voice_id: str = Form(None),
    avatar_file: UploadFile = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate video for a lesson"""
    # Verify lesson belongs to current user
    lesson = db.query(Lesson).join(LearningPath).join(Topic).filter(
        Lesson.id == lesson_id,
        Topic.user_id == current_user.id
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Use user's default voice if not specified
    if not voice_id:
        voice_id = current_user.voice_id
    
    if not voice_id:
        raise HTTPException(
            status_code=400, 
            detail="No voice specified. Please set a default voice or provide voice_id"
        )
    
    # Handle avatar image
    avatar_path = None
    if avatar_file:
        # Save uploaded avatar
        avatar_filename = f"{uuid.uuid4()}_{avatar_file.filename}"
        avatar_path = os.path.join(settings.UPLOAD_DIR, "avatars", avatar_filename)
        
        os.makedirs(os.path.dirname(avatar_path), exist_ok=True)
        with open(avatar_path, "wb") as f:
            content = await avatar_file.read()
            f.write(content)
    elif current_user.avatar_url:
        # Use user's default avatar
        avatar_path = current_user.avatar_url
    else:
        raise HTTPException(
            status_code=400,
            detail="No avatar specified. Please upload an avatar or set a default avatar"
        )
    
    # Create video record
    db_video = Video(
        title=f"Video for {lesson.title}",
        video_url="",  # Will be updated after generation
        lesson_id=lesson_id,
        voice_id=voice_id,
        avatar_url=avatar_path,
        status="processing"
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    
    # Add background task for video generation
    lesson_text = lesson.script or lesson.content
    background_tasks.add_task(
        generate_video_task, 
        db_video.id, 
        lesson_text, 
        voice_id, 
        avatar_path
    )
    
    return {
        "message": "Video generation started", 
        "video_id": db_video.id, 
        "status": "processing"
    }

@router.get("/lesson/{lesson_id}", response_model=List[dict])
def get_videos_by_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all videos for a specific lesson"""
    # Verify lesson belongs to current user
    lesson = db.query(Lesson).join(LearningPath).join(Topic).filter(
        Lesson.id == lesson_id,
        Topic.user_id == current_user.id
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    videos = db.query(Video).filter(Video.lesson_id == lesson_id).all()
    return [
        {
            "id": video.id,
            "title": video.title,
            "video_url": video.video_url,
            "audio_url": video.audio_url,
            "transcript": video.transcript,
            "duration": video.duration,
            "status": video.status,
            "lesson_id": video.lesson_id,
            "voice_id": video.voice_id,
            "avatar_url": video.avatar_url,
            "created_at": video.created_at
        }
        for video in videos
    ]

@router.get("/{video_id}", response_model=dict)
def get_video(
    video_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific video details"""
    video = db.query(Video).join(Lesson).join(LearningPath).join(Topic).filter(
        Video.id == video_id,
        Topic.user_id == current_user.id
    ).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return {
        "id": video.id,
        "title": video.title,
        "video_url": video.video_url,
        "audio_url": video.audio_url,
        "transcript": video.transcript,
        "duration": video.duration,
        "status": video.status,
        "lesson_id": video.lesson_id,
        "voice_id": video.voice_id,
        "avatar_url": video.avatar_url,
        "created_at": video.created_at
    }

@router.delete("/{video_id}")
def delete_video(
    video_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a video"""
    video = db.query(Video).join(Lesson).join(LearningPath).join(Topic).filter(
        Video.id == video_id,
        Topic.user_id == current_user.id
    ).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Delete video files
    if video.video_url and os.path.exists(video.video_url.replace("/uploads/", settings.UPLOAD_DIR + "/")):
        os.remove(video.video_url.replace("/uploads/", settings.UPLOAD_DIR + "/"))
    
    if video.audio_url and os.path.exists(video.audio_url.replace("/uploads/", settings.UPLOAD_DIR + "/")):
        os.remove(video.audio_url.replace("/uploads/", settings.UPLOAD_DIR + "/"))
    
    db.delete(video)
    db.commit()
    
    return {"message": "Video deleted successfully"}

