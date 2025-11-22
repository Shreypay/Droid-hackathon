"""
Convert audio to ElevenLabs-compatible format
MP3 192kbps, 44.1kHz, 16-bit
"""

import os
import subprocess
import sys

# Find the most recent audio file
audio_dir = "processed/extracted"
audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]
audio_files.sort()
input_audio = os.path.join(audio_dir, audio_files[-1])

output_audio = input_audio.replace('.wav', '_elevenlabs.mp3')

print("=" * 60)
print("CONVERTING AUDIO FOR ELEVENLABS")
print("=" * 60)
print()
print(f"Input:  {input_audio}")
print(f"Output: {output_audio}")
print()

# Convert with exact ElevenLabs specifications
cmd = [
    'ffmpeg',
    '-i', input_audio,
    '-acodec', 'libmp3lame',  # MP3 codec
    '-ar', '44100',           # 44.1kHz sample rate
    '-ac', '1',               # Mono
    '-b:a', '192k',           # 192kbps bitrate
    '-sample_fmt', 's16',     # 16-bit
    '-y',
    output_audio
]

print("🔄 Converting...")
try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print("✅ Conversion complete!")
    print()
    print(f"File size: {os.path.getsize(output_audio) / 1024:.1f} KB")
    print()
    print("Now test with:")
    print(f"  python test_voice_clone_v2.py")
    
except subprocess.CalledProcessError as e:
    print("❌ Conversion failed!")
    print(e.stderr)
    sys.exit(1)