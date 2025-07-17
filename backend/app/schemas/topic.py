from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None

class TopicCreate(TopicBase):
    pass

class TopicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TopicInDBBase(TopicBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Topic(TopicInDBBase):
    pass

class LearningPathBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_weeks: int = 6

class LearningPathCreate(LearningPathBase):
    topic_id: int

class LearningPathUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_weeks: Optional[int] = None

class LearningPathInDBBase(LearningPathBase):
    id: int
    topic_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LearningPath(LearningPathInDBBase):
    pass

class LessonBase(BaseModel):
    title: str
    content: str
    script: Optional[str] = None
    week_number: int
    day_number: int

class LessonCreate(LessonBase):
    learning_path_id: int

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    script: Optional[str] = None
    week_number: Optional[int] = None
    day_number: Optional[int] = None

class LessonInDBBase(LessonBase):
    id: int
    learning_path_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Lesson(LessonInDBBase):
    pass

