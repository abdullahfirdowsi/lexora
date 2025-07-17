from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    video_url = Column(String, nullable=False)
    audio_url = Column(String, nullable=True)
    transcript = Column(Text, nullable=True)
    duration = Column(Float, nullable=True)  # Duration in seconds
    status = Column(String, default="processing")  # processing, completed, failed
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    
    # Generation metadata
    voice_id = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lesson = relationship("Lesson", back_populates="videos")

