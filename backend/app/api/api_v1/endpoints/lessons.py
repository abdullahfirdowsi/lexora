from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.models.topic import Topic
from app.models.learning_path import LearningPath
from app.models.lesson import Lesson
from app.schemas.topic import Lesson as LessonSchema, LessonCreate, LessonUpdate

router = APIRouter()

@router.post("/", response_model=LessonSchema)
def create_lesson(
    lesson_data: LessonCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify learning path belongs to current user
    learning_path = db.query(LearningPath).join(Topic).filter(
        LearningPath.id == lesson_data.learning_path_id,
        Topic.user_id == current_user.id
    ).first()
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    db_lesson = Lesson(
        title=lesson_data.title,
        content=lesson_data.content,
        script=lesson_data.script,
        week_number=lesson_data.week_number,
        day_number=lesson_data.day_number,
        learning_path_id=lesson_data.learning_path_id
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    
    return db_lesson

@router.get("/learning-path/{learning_path_id}", response_model=List[LessonSchema])
def read_lessons_by_learning_path(
    learning_path_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify learning path belongs to current user
    learning_path = db.query(LearningPath).join(Topic).filter(
        LearningPath.id == learning_path_id,
        Topic.user_id == current_user.id
    ).first()
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    lessons = db.query(Lesson).filter(Lesson.learning_path_id == learning_path_id).all()
    return lessons

@router.get("/{lesson_id}", response_model=LessonSchema)
def read_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).join(LearningPath).join(Topic).filter(
        Lesson.id == lesson_id,
        Topic.user_id == current_user.id
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.put("/{lesson_id}", response_model=LessonSchema)
def update_lesson(
    lesson_id: int,
    lesson_update: LessonUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).join(LearningPath).join(Topic).filter(
        Lesson.id == lesson_id,
        Topic.user_id == current_user.id
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    update_data = lesson_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lesson, field, value)
    
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    
    return lesson

@router.delete("/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).join(LearningPath).join(Topic).filter(
        Lesson.id == lesson_id,
        Topic.user_id == current_user.id
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    db.delete(lesson)
    db.commit()
    
    return {"message": "Lesson deleted successfully"}

