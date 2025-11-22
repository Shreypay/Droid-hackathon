"""
Test voice cloning with file handle method
"""

import os
import sys
sys.path.insert(0, 'Analyzer')

from config import ELEVENLABS_API_KEY
from elevenlabs.client import ElevenLabs

print("=" * 60)
print("TESTING VOICE CLONING - FILE HANDLE METHOD")
print("=" * 60)
print()

# Initialize client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Find the converted MP3
audio_dir = "processed/extracted"
mp3_files = [f for f in os.listdir(audio_dir) if f.endswith('_elevenlabs.mp3')]

if not mp3_files:
    print("❌ No converted audio found!")
    sys.exit(1)

mp3_path = os.path.join(audio_dir, mp3_files[-1])

print(f"📁 Audio file: {mp3_path}")
print(f"📊 File size: {os.path.getsize(mp3_path) / 1024:.1f} KB")
print()

# Method 1: Try with file handle (tuple format)
print("🎤 Method 1: Trying with (filename, file_handle) tuple...")
try:
    with open(mp3_path, 'rb') as f:
        voice = client.voices.ivc.create(
            name="Test_Clone_Handle",
            description="Testing with file handle",
            files=[(os.path.basename(mp3_path), f)]
        )
    
    print("=" * 60)
    print("🎉 SUCCESS WITH METHOD 1!")
    print("=" * 60)
    print(f"Voice ID: {voice.voice_id}")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Method 1 failed: {str(e)[:200]}")
    print()

# Method 2: Try reading file as bytes
print("🎤 Method 2: Trying with file bytes...")
try:
    with open(mp3_path, 'rb') as f:
        file_bytes = f.read()
    
    voice = client.voices.ivc.create(
        name="Test_Clone_Bytes",
        description="Testing with bytes",
        files=[(os.path.basename(mp3_path), file_bytes)]
    )
    
    print("=" * 60)
    print("🎉 SUCCESS WITH METHOD 2!")
    print("=" * 60)
    print(f"Voice ID: {voice.voice_id}")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Method 2 failed: {str(e)[:200]}")
    print()

# Method 3: Try with just file path as string
print("🎤 Method 3: Trying with file path string...")
try:
    voice = client.voices.ivc.create(
        name="Test_Clone_Path",
        description="Testing with path",
        files=[mp3_path]
    )
    
    print("=" * 60)
    print("🎉 SUCCESS WITH METHOD 3!")
    print("=" * 60)
    print(f"Voice ID: {voice.voice_id}")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Method 3 failed: {str(e)[:200]}")
    print()

print("=" * 60)
print("❌ ALL METHODS FAILED")
print("=" * 60)
print()
print("This might be an API permissions issue.")
print()
print("Please verify in your ElevenLabs dashboard:")
print("1. Go to: https://elevenlabs.io/app/settings/api-keys")
print("2. Check your API key has:")
print("   - 'Voices' set to 'Write'")
print("   - 'Text to Speech' set to 'Access'")
print("3. Make sure you're on Starter plan or higher")
print()
print("You can also try creating a voice clone manually in the")
print("ElevenLabs dashboard to verify your account has this feature.")