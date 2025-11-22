"""
Video to Audio Extractor
Extracts audio from video files using FFmpeg
"""

import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

class VideoProcessor:
    """Extract audio from video files"""
    
    def __init__(self, output_dir: str = "processed/extracted"):
        """
        Initialize the video processor
        
        Args:
            output_dir: Where to save extracted audio files
        """
        self.output_dir = output_dir
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    def extract_audio(self, video_path: str) -> str:
        """
        Extract audio from video file
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Path to the extracted audio file (.wav format)
        """
        # Check if video file exists
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Create output filename
        timestamp = int(datetime.now().timestamp())
        output_filename = f"audio_{timestamp}.wav"
        output_path = os.path.join(self.output_dir, output_filename)
        
        # FFmpeg command
        command = [
            'ffmpeg',
            '-i', video_path,        # Input video
            '-vn',                    # No video (audio only)
            '-acodec', 'pcm_s16le',  # Audio codec for WAV
            '-ar', '16000',           # 16kHz sample rate (good for speech)
            '-ac', '1',               # Mono audio
            '-y',                     # Overwrite if exists
            output_path
        ]
        
        print(f"Extracting audio from: {video_path}")
        
        # Run FFmpeg
        try:
            subprocess.run(command, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg failed: {e.stderr.decode()}")
        
        # Check if output was created
        if not os.path.exists(output_path):
            raise Exception("Audio extraction failed")
        
        print(f"Audio saved to: {output_path}")
        return output_path


# TEST CODE - Run this file directly to test
if __name__ == "__main__":
    print("=" * 50)
    print("VIDEO TO AUDIO EXTRACTOR TEST")
    print("=" * 50)
    print()
    
    # Initialize processor
    processor = VideoProcessor()
    
    # Look for test video
    test_video = "test_video.mp4"
    
    if not os.path.exists(test_video):
        print(f"❌ Test video not found: {test_video}")
        print()
        print("Please place a video file named 'test_video.mp4' in the project root")
        print("(Same folder as the Analyzer folder)")
        sys.exit(1)
    
    print(f"✅ Found video: {test_video}")
    print()
    
    # Extract audio
    try:
        audio_path = processor.extract_audio(test_video)
        print()
        print("=" * 50)
        print("✅ SUCCESS!")
        print("=" * 50)
        print(f"Audio file: {audio_path}")
        print(f"File size: {os.path.getsize(audio_path) / 1024:.1f} KB")
        print()
        print("Check the 'processed/extracted/' folder to find your audio file")
        
    except Exception as e:
        print()
        print("=" * 50)
        print("❌ ERROR")
        print("=" * 50)
        print(f"Error: {str(e)}")
        print()
        print("Make sure FFmpeg is installed:")
        print("  Mac:     brew install ffmpeg")
        print("  Ubuntu:  sudo apt-get install ffmpeg")
        print("  Windows: Download from ffmpeg.org")