import os
import httpx
import aiofiles
import base64
from typing import Dict, Optional
from app.core.config import settings

class VideoGenerationService:
    def __init__(self):
        self.api_key = settings.HUGGINGFACE_API_KEY
        self.suprath_url = settings.SUPRATH_LIPSYNC_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def generate_lipsync_video(
        self, 
        audio_path: str, 
        image_path: str, 
        output_path: str
    ) -> bool:
        """Generate lip-sync video using Suprath-lipsync API"""
        if not self.api_key:
            print("Hugging Face API key not configured")
            return False
        
        try:
            # Read and encode files
            async with aiofiles.open(audio_path, 'rb') as f:
                audio_content = await f.read()
                audio_b64 = base64.b64encode(audio_content).decode('utf-8')
            
            async with aiofiles.open(image_path, 'rb') as f:
                image_content = await f.read()
                image_b64 = base64.b64encode(image_content).decode('utf-8')
            
            # Prepare request data
            data = {
                "data": [
                    f"data:audio/wav;base64,{audio_b64}",
                    f"data:image/jpeg;base64,{image_b64}"
                ]
            }
            
            # Make API request
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    self.suprath_url,
                    headers=self.headers,
                    json=data
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Check if generation was successful
                if "data" in result and len(result["data"]) > 0:
                    video_data = result["data"][0]
                    
                    # If video_data is a base64 string, decode and save
                    if isinstance(video_data, str) and video_data.startswith("data:video"):
                        # Extract base64 data
                        video_b64 = video_data.split(",")[1]
                        video_bytes = base64.b64decode(video_b64)
                        
                        # Save video file
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        async with aiofiles.open(output_path, 'wb') as f:
                            await f.write(video_bytes)
                        
                        return True
                    elif isinstance(video_data, str) and video_data.startswith("http"):
                        # If it's a URL, download the video
                        async with httpx.AsyncClient() as download_client:
                            video_response = await download_client.get(video_data)
                            video_response.raise_for_status()
                            
                            os.makedirs(os.path.dirname(output_path), exist_ok=True)
                            async with aiofiles.open(output_path, 'wb') as f:
                                await f.write(video_response.content)
                            
                            return True
                
                return False
                
        except Exception as e:
            print(f"Error generating lip-sync video: {e}")
            return False

    async def generate_video_from_lesson(
        self,
        lesson_text: str,
        voice_id: str,
        avatar_image_path: str,
        output_video_path: str,
        output_audio_path: str
    ) -> Dict[str, any]:
        """Generate complete video lesson with audio and lip-sync"""
        try:
            # Import ElevenLabs service
            from app.services.elevenlabs_service import elevenlabs_service
            
            # Step 1: Generate audio from text
            audio_success = await elevenlabs_service.generate_speech(
                text=lesson_text,
                voice_id=voice_id,
                output_path=output_audio_path
            )
            
            if not audio_success:
                return {
                    "success": False,
                    "error": "Failed to generate audio"
                }
            
            # Step 2: Generate lip-sync video
            video_success = await self.generate_lipsync_video(
                audio_path=output_audio_path,
                image_path=avatar_image_path,
                output_path=output_video_path
            )
            
            if not video_success:
                return {
                    "success": False,
                    "error": "Failed to generate lip-sync video"
                }
            
            return {
                "success": True,
                "video_path": output_video_path,
                "audio_path": output_audio_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Video generation failed: {str(e)}"
            }

    async def create_simple_video_with_audio(
        self,
        audio_path: str,
        image_path: str,
        output_path: str,
        duration: Optional[float] = None
    ) -> bool:
        """Create a simple video by combining static image with audio (fallback method)"""
        try:
            import subprocess
            
            # Use ffmpeg to create video from image and audio
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", image_path,
                "-i", audio_path,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",
                output_path
            ]
            
            if duration:
                cmd.extend(["-t", str(duration)])
            
            # Run ffmpeg command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return True
            else:
                print(f"FFmpeg error: {stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"Error creating simple video: {e}")
            return False

# Create a singleton instance
video_service = VideoGenerationService()

