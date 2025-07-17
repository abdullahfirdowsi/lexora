from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.put("/me/preferences", response_model=UserSchema)
def update_user_preferences(
    avatar_url: str = None,
    voice_id: str = None,
    voice_name: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if avatar_url is not None:
        current_user.avatar_url = avatar_url
    if voice_id is not None:
        current_user.voice_id = voice_id
    if voice_name is not None:
        current_user.voice_name = voice_name
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return current_user

