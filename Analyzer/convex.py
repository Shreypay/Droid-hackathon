"""
Convex Database Client
Stores all session data in Convex
"""

import os
import requests
import base64
from datetime import datetime

class ConvexClient:
    """Store and retrieve speech surgery session data"""
    
    def __init__(self, deployment_url: str):
        """
        Initialize Convex client
        
        Args:
            deployment_url: Your Convex deployment URL
        """
        self.deployment_url = deployment_url.rstrip('/')
    
    def store_session(self, session_data: dict) -> dict:
        """
        Store complete session in Convex
        
        Args:
            session_data: Dictionary containing:
                - video_path: Path to original video
                - audio_path: Path to extracted audio
                - transcript_json_path: Path to transcript JSON
                - transcript_csv_path: Path to transcript CSV
                - fixed_transcript_path: Path to cleaned transcript
                - improved_audio_mp3_path: Path to improved MP3
                - improved_audio_wav_path: Path to improved WAV
                - transcript_text: Full transcript text
                - cleaned_text: Cleaned transcript text
                - metadata: Dict with duration, word_count, etc.
        
        Returns:
            Response from Convex with session ID
        """
        print("📤 Uploading to Convex database...")
        
        try:
            # Read all files as base64
            files_data = {}
            
            # Video file
            if os.path.exists(session_data['video_path']):
                files_data['video'] = self._file_to_base64(session_data['video_path'])
                files_data['video_name'] = os.path.basename(session_data['video_path'])
            
            # Original audio
            if os.path.exists(session_data['audio_path']):
                files_data['original_audio'] = self._file_to_base64(session_data['audio_path'])
                files_data['original_audio_name'] = os.path.basename(session_data['audio_path'])
            
            # Transcript JSON
            if os.path.exists(session_data['transcript_json_path']):
                with open(session_data['transcript_json_path'], 'r') as f:
                    files_data['transcript_json'] = f.read()
            
            # Transcript CSV
            if os.path.exists(session_data['transcript_csv_path']):
                with open(session_data['transcript_csv_path'], 'r') as f:
                    files_data['transcript_csv'] = f.read()
            
            # Fixed transcript CSV
            if os.path.exists(session_data['fixed_transcript_path']):
                with open(session_data['fixed_transcript_path'], 'r') as f:
                    files_data['fixed_transcript_csv'] = f.read()
            
            # Improved audio MP3
            if os.path.exists(session_data['improved_audio_mp3_path']):
                files_data['improved_audio_mp3'] = self._file_to_base64(session_data['improved_audio_mp3_path'])
            
            # Improved audio WAV
            if os.path.exists(session_data['improved_audio_wav_path']):
                files_data['improved_audio_wav'] = self._file_to_base64(session_data['improved_audio_wav_path'])
                files_data['improved_audio_name'] = os.path.basename(session_data['improved_audio_wav_path'])
            
            # Prepare payload
            payload = {
                'userId': session_data.get('user_id', 'default_user'),
                'timestamp': int(datetime.now().timestamp() * 1000),
                'transcriptText': session_data['transcript_text'],
                'cleanedText': session_data['cleaned_text'],
                'metadata': session_data['metadata'],
                'files': files_data
            }
            
            # Send to Convex
            response = requests.post(
                f"{self.deployment_url}/sessions/create",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=120  # 2 minutes for large files
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Uploaded to Convex successfully!")
                print(f"   Session ID: {result.get('sessionId', 'unknown')}")
                return result
            else:
                raise Exception(f"Convex upload failed: {response.status_code} - {response.text}")
        
        except Exception as e:
            print(f"❌ Failed to upload to Convex: {str(e)}")
            raise
    
    def _file_to_base64(self, file_path: str) -> str:
        """Convert file to base64 string"""
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def get_session(self, session_id: str) -> dict:
        """Retrieve session from Convex"""
        try:
            response = requests.get(
                f"{self.deployment_url}/sessions/{session_id}",
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get session: {response.status_code}")
        
        except Exception as e:
            print(f"❌ Failed to retrieve from Convex: {str(e)}")
            raise
    
    def list_sessions(self, user_id: str = 'default_user') -> list:
        """List all sessions for a user"""
        try:
            response = requests.get(
                f"{self.deployment_url}/sessions/list",
                params={'userId': user_id},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to list sessions: {response.status_code}")
        
        except Exception as e:
            print(f"❌ Failed to list sessions: {str(e)}")
            raise


# TEST CODE
if __name__ == "__main__":
    print("=" * 60)
    print("CONVEX CLIENT TEST")
    print("=" * 60)
    print()
    
    try:
        from config import CONVEX_URL
    except ImportError:
        print("❌ CONVEX_URL not found in config.py")
        print()
        print("Add to Analyzer/config.py:")
        print("  CONVEX_URL = 'https://your-deployment.convex.cloud'")
        exit(1)
    
    if not CONVEX_URL or CONVEX_URL == "":
        print("❌ CONVEX_URL is empty in config.py")
        print()
        print("Set your Convex deployment URL in config.py")
        exit(1)
    
    client = ConvexClient(CONVEX_URL)
    
    print(f"✅ Convex client initialized")
    print(f"   URL: {CONVEX_URL}")
    print()
    print("Ready to use! Run main.py to upload session data.")