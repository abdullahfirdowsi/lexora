from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import os
import uuid

from app.core.deps import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.services.elevenlabs_service import elevenlabs_service
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_voices(current_user: User = Depends(get_current_active_user)):
    """Get all available voices from ElevenLabs"""
    voices = await elevenlabs_service.get_voices()
    return voices

@router.get("/{voice_id}", response_model=dict)
async def get_voice(
    voice_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get specific voice details"""
    voice = await elevenlabs_service.get_voice_by_id(voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")
    return voice

@router.post("/clone", response_model=dict)
async def clone_voice(
    name: str = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Clone a voice using uploaded audio files"""
    if not settings.ELEVENLABS_API_KEY:
        raise HTTPException(
            status_code=503, 
            detail="ElevenLabs API key not configured"
        )
    
    if len(files) < 1:
        raise HTTPException(
            status_code=400,
            detail="At least one audio file is required for voice cloning"
        )
    
    # Read file contents
    file_contents = []
    for file in files:
        if not file.content_type.startswith('audio/'):
            raise HTTPException(
                status_code=400,
                detail=f"File {file.filename} is not an audio file"
            )
        
        content = await file.read()
        file_contents.append(content)
    
    # Clone voice
    result = await elevenlabs_service.clone_voice(name, description, file_contents)
    if not result:
        raise HTTPException(
            status_code=500,
            detail="Failed to clone voice"
        )
    
    return result

@router.post("/generate-speech", response_model=dict)
async def generate_speech(
    text: str = Form(...),
    voice_id: str = Form(...),
    stability: float = Form(0.5),
    similarity_boost: float = Form(0.5),
    current_user: User = Depends(get_current_active_user)
):
    """Generate speech from text using specified voice"""
    if not settings.ELEVENLABS_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs API key not configured"
        )
    
    if len(text) > 5000:
        raise HTTPException(
            status_code=400,
            detail="Text is too long. Maximum 5000 characters allowed."
        )
    
    # Generate unique filename
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join(settings.UPLOAD_DIR, "audio", audio_filename)
    
    # Voice settings
    voice_settings = {
        "stability": stability,
        "similarity_boost": similarity_boost
    }
    
    # Generate speech
    success = await elevenlabs_service.generate_speech(
        text=text,
        voice_id=voice_id,
        output_path=audio_path,
        voice_settings=voice_settings
    )
    
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate speech"
        )
    
    # Return audio file URL
    audio_url = f"/uploads/audio/{audio_filename}"
    return {
        "audio_url": audio_url,
        "text": text,
        "voice_id": voice_id,
        "voice_settings": voice_settings
    }

@router.delete("/{voice_id}")
async def delete_voice(
    voice_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a cloned voice"""
    if not settings.ELEVENLABS_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs API key not configured"
        )
    
    success = await elevenlabs_service.delete_voice(voice_id)
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete voice"
        )
    
    return {"message": "Voice deleted successfully"}

@router.get("/user/info", response_model=dict)
async def get_user_info(current_user: User = Depends(get_current_active_user)):
    """Get ElevenLabs user subscription info"""
    if not settings.ELEVENLABS_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs API key not configured"
        )
    
    user_info = await elevenlabs_service.get_user_info()
    if not user_info:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch user info"
        )
    
    return user_info

