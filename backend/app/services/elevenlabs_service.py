import os
import httpx
import aiofiles
from typing import List, Dict, Optional
from app.core.config import settings

class ElevenLabsService:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "Accept": "application/json",
            "xi-api-key": self.api_key
        }

    async def get_voices(self) -> List[Dict]:
        """Get all available voices from ElevenLabs"""
        if not self.api_key:
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/voices",
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                return data.get("voices", [])
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return []

    async def get_voice_by_id(self, voice_id: str) -> Optional[Dict]:
        """Get specific voice details by ID"""
        if not self.api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/voices/{voice_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error fetching voice {voice_id}: {e}")
            return None

    async def clone_voice(self, name: str, description: str, files: List[bytes]) -> Optional[Dict]:
        """Clone a voice using uploaded audio files"""
        if not self.api_key:
            return None
        
        try:
            # Prepare files for upload
            files_data = []
            for i, file_content in enumerate(files):
                files_data.append(("files", (f"sample_{i}.wav", file_content, "audio/wav")))
            
            data = {
                "name": name,
                "description": description
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/voices/add",
                    headers={"xi-api-key": self.api_key},
                    data=data,
                    files=files_data
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error cloning voice: {e}")
            return None

    async def generate_speech(
        self, 
        text: str, 
        voice_id: str, 
        output_path: str,
        model_id: str = "eleven_monolingual_v1",
        voice_settings: Optional[Dict] = None
    ) -> bool:
        """Generate speech from text using specified voice"""
        if not self.api_key:
            return False
        
        if voice_settings is None:
            voice_settings = {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        
        try:
            data = {
                "text": text,
                "model_id": model_id,
                "voice_settings": voice_settings
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/text-to-speech/{voice_id}",
                    headers={
                        "Accept": "audio/mpeg",
                        "Content-Type": "application/json",
                        "xi-api-key": self.api_key
                    },
                    json=data
                )
                response.raise_for_status()
                
                # Save audio file
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                async with aiofiles.open(output_path, 'wb') as f:
                    await f.write(response.content)
                
                return True
        except Exception as e:
            print(f"Error generating speech: {e}")
            return False

    async def delete_voice(self, voice_id: str) -> bool:
        """Delete a cloned voice"""
        if not self.api_key:
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/voices/{voice_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"Error deleting voice {voice_id}: {e}")
            return False

    async def get_user_info(self) -> Optional[Dict]:
        """Get user subscription info"""
        if not self.api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/user",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error fetching user info: {e}")
            return None

# Create a singleton instance
elevenlabs_service = ElevenLabsService()

