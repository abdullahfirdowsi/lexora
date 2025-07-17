from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.models.topic import Topic
from app.models.learning_path import LearningPath
from app.schemas.topic import LearningPath as LearningPathSchema, LearningPathCreate, LearningPathUpdate

router = APIRouter()

@router.post("/", response_model=LearningPathSchema)
def create_learning_path(
    learning_path_data: LearningPathCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify topic belongs to current user
    topic = db.query(Topic).filter(
        Topic.id == learning_path_data.topic_id,
        Topic.user_id == current_user.id
    ).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    db_learning_path = LearningPath(
        title=learning_path_data.title,
        description=learning_path_data.description,
        duration_weeks=learning_path_data.duration_weeks,
        topic_id=learning_path_data.topic_id
    )
    db.add(db_learning_path)
    db.commit()
    db.refresh(db_learning_path)
    
    return db_learning_path

@router.get("/topic/{topic_id}", response_model=List[LearningPathSchema])
def read_learning_paths_by_topic(
    topic_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify topic belongs to current user
    topic = db.query(Topic).filter(Topic.id == topic_id, Topic.user_id == current_user.id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    learning_paths = db.query(LearningPath).filter(LearningPath.topic_id == topic_id).all()
    return learning_paths

@router.get("/{learning_path_id}", response_model=LearningPathSchema)
def read_learning_path(
    learning_path_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    learning_path = db.query(LearningPath).join(Topic).filter(
        LearningPath.id == learning_path_id,
        Topic.user_id == current_user.id
    ).first()
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return learning_path

@router.put("/{learning_path_id}", response_model=LearningPathSchema)
def update_learning_path(
    learning_path_id: int,
    learning_path_update: LearningPathUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    learning_path = db.query(LearningPath).join(Topic).filter(
        LearningPath.id == learning_path_id,
        Topic.user_id == current_user.id
    ).first()
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    update_data = learning_path_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(learning_path, field, value)
    
    db.add(learning_path)
    db.commit()
    db.refresh(learning_path)
    
    return learning_path

@router.delete("/{learning_path_id}")
def delete_learning_path(
    learning_path_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    learning_path = db.query(LearningPath).join(Topic).filter(
        LearningPath.id == learning_path_id,
        Topic.user_id == current_user.id
    ).first()
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    db.delete(learning_path)
    db.commit()
    
    return {"message": "Learning path deleted successfully"}

