from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.models.topic import Topic
from app.schemas.topic import Topic as TopicSchema, TopicCreate, TopicUpdate

router = APIRouter()

@router.post("/", response_model=TopicSchema)
def create_topic(
    topic_data: TopicCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_topic = Topic(
        title=topic_data.title,
        description=topic_data.description,
        user_id=current_user.id
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    
    return db_topic

@router.get("/", response_model=List[TopicSchema])
def read_topics(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    topics = db.query(Topic).filter(Topic.user_id == current_user.id).offset(skip).limit(limit).all()
    return topics

@router.get("/{topic_id}", response_model=TopicSchema)
def read_topic(
    topic_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    topic = db.query(Topic).filter(Topic.id == topic_id, Topic.user_id == current_user.id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.put("/{topic_id}", response_model=TopicSchema)
def update_topic(
    topic_id: int,
    topic_update: TopicUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    topic = db.query(Topic).filter(Topic.id == topic_id, Topic.user_id == current_user.id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    update_data = topic_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(topic, field, value)
    
    db.add(topic)
    db.commit()
    db.refresh(topic)
    
    return topic

@router.delete("/{topic_id}")
def delete_topic(
    topic_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    topic = db.query(Topic).filter(Topic.id == topic_id, Topic.user_id == current_user.id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    db.delete(topic)
    db.commit()
    
    return {"message": "Topic deleted successfully"}

