from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    script = Column(Text, nullable=True)  # AI-generated script for narration
    week_number = Column(Integer, nullable=False)
    day_number = Column(Integer, nullable=False)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    learning_path = relationship("LearningPath", back_populates="lessons")
    videos = relationship("Video", back_populates="lesson")
    progress = relationship("Progress", back_populates="lesson")

