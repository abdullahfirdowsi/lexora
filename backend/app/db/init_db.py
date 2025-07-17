from app.db.database import engine, Base
from app.models import user, topic, learning_path, lesson, video, progress, asset

def init_db():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)

