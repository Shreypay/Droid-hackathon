"""
Audio Creation using ElevenLabs Voice Cloning
Creates new audio with cleaned transcript using original speaker's voice
"""

import os
import csv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

class AudioCreator:
    """Generate audio with voice cloning"""
    
    def __init__(self, api_key: str):
        """
        Initialize ElevenLabs client
        
        Args:
            api_key: Your ElevenLabs API key
        """
        self.client = ElevenLabs(api_key=api_key)
    
    def clone_voice_and_generate(self, original_audio_path: str, 
                                fixed_transcript_csv: str, 
                                output_path: str = "processed/improved_audio.mp3") -> str:
        """
        Clone voice from original audio and generate new audio with cleaned text
        
        Args:
            original_audio_path: Path to original audio file (.wav)
            fixed_transcript_csv: Path to fixed transcript CSV
            output_path: Where to save the new audio
            
        Returns:
            Path to generated audio file
        """
        # Read the cleaned transcript
        print(f"📖 Reading cleaned transcript from: {fixed_transcript_csv}")
        
        if not os.path.exists(fixed_transcript_csv):
            raise FileNotFoundError(f"Fixed transcript not found: {fixed_transcript_csv}")
        
        with open(fixed_transcript_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            cleaned_text = next(reader)[0]
        
        print(f"✅ Loaded cleaned text ({len(cleaned_text)} characters)")
        print()
        
        # Step 1: Prepare audio for cloning (convert to MP3 format)
        print("🎤 Preparing audio for voice cloning...")
        print(f"   Source: {original_audio_path}")
        
        # Create an MP3 version for cloning (ElevenLabs prefers MP3)
        import subprocess
        temp_audio_for_cloning = original_audio_path.replace('.wav', '_clone.mp3')
        
        try:
            # Convert to high-quality MP3 for cloning (ElevenLabs specs)
            subprocess.run([
                'ffmpeg', '-i', original_audio_path,
                '-acodec', 'libmp3lame',
                '-ar', '44100',      # 44.1kHz sample rate
                '-ac', '1',          # Mono
                '-b:a', '192k',      # 192kbps bitrate
                '-sample_fmt', 's16', # 16-bit
                '-y',
                temp_audio_for_cloning
            ], check=True, capture_output=True, timeout=30)
            
            cloning_audio_path = temp_audio_for_cloning
            
            # Check file size
            file_size = os.path.getsize(cloning_audio_path) / 1024  # KB
            print(f"✅ Audio prepared for cloning ({file_size:.1f} KB)")
            
            if file_size < 50:
                print(f"⚠️ Warning: Audio file is very small ({file_size:.1f} KB)")
                print("   Voice cloning works best with 30+ seconds of audio")
            
        except Exception as e:
            print(f"⚠️ Audio preparation failed: {str(e)}")
            print("   Cannot proceed with voice cloning")
            raise
        
        print()
        
        # Step 2: Clone voice using correct file handle method
        print("🎤 Cloning voice from audio...")
        
        voice_id = None
        
        try:
            # IMPORTANT: Pass file as (filename, file_handle) tuple
            with open(cloning_audio_path, 'rb') as audio_file:
                voice = self.client.voices.ivc.create(
                    name="Cloned_Speaker",
                    description="Voice cloned from original audio",
                    files=[(os.path.basename(cloning_audio_path), audio_file)]
                )
            
            voice_id = voice.voice_id
            print(f"✅ Voice cloned successfully! Voice ID: {voice_id}")
            
            # Clean up temp file
            if os.path.exists(temp_audio_for_cloning):
                os.remove(temp_audio_for_cloning)
            
            print()
            
        except Exception as e:
            # Clean up temp file
            if os.path.exists(temp_audio_for_cloning):
                os.remove(temp_audio_for_cloning)
            
            error_msg = str(e)
            print(f"⚠️ Voice cloning failed:")
            print(f"   {error_msg}")
            print()
            print("   Using high-quality default voice instead...")
            
            # Use a high-quality default voice
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel - Natural and clear
            print(f"   Voice ID: {voice_id}")
            print()
        
        # Step 2: Generate audio with cloned voice
        print("🎵 Generating new audio with cleaned transcript...")
        
        try:
            audio_generator = self.client.text_to_speech.convert(
                voice_id=voice_id,
                text=cleaned_text,
                model_id="eleven_multilingual_v2",
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.0,
                    use_speaker_boost=True
                )
            )
            
            # Save the audio
            print(f"💾 Saving to: {output_path}")
            
            with open(output_path, 'wb') as f:
                for chunk in audio_generator:
                    f.write(chunk)
            
            print(f"✅ Audio generated successfully!")
            print(f"   Output: {output_path}")
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Audio generation failed: {str(e)}")
    
    def generate_with_default_voice(self, fixed_transcript_csv: str,
                                   output_path: str = "processed/improved_audio.mp3",
                                   voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> str:
        """
        Generate audio with a default voice (no cloning)
        
        Args:
            fixed_transcript_csv: Path to fixed transcript CSV
            output_path: Where to save the audio
            voice_id: ElevenLabs voice ID to use
            
        Returns:
            Path to generated audio file
        """
        # Read the cleaned transcript
        print(f"📖 Reading cleaned transcript from: {fixed_transcript_csv}")
        
        with open(fixed_transcript_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            cleaned_text = next(reader)[0]
        
        print(f"✅ Loaded cleaned text ({len(cleaned_text)} characters)")
        print()
        
        # Generate audio
        print(f"🎵 Generating audio with voice ID: {voice_id}")
        
        try:
            audio_generator = self.client.text_to_speech.convert(
                voice_id=voice_id,
                text=cleaned_text,
                model_id="eleven_multilingual_v2"
            )
            
            # Save the audio
            with open(output_path, 'wb') as f:
                for chunk in audio_generator:
                    f.write(chunk)
            
            print(f"✅ Audio generated successfully!")
            print(f"   Output: {output_path}")
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Audio generation failed: {str(e)}")


# TEST CODE
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("AUDIO CREATION TEST")
    print("=" * 60)
    print()
    
    # Get API key
    api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not api_key:
        try:
            from config import ELEVENLABS_API_KEY
            api_key = ELEVENLABS_API_KEY
        except ImportError:
            pass
    
    if not api_key:
        if len(sys.argv) > 1:
            api_key = sys.argv[1]
            print("✅ Using API key from argument")
        else:
            print("❌ ElevenLabs API key not found!")
            print()
            print("Option 1: Add to Analyzer/config.py:")
            print("  ELEVENLABS_API_KEY = 'your_key'")
            print()
            print("Option 2: Set environment variable:")
            print("  export ELEVENLABS_API_KEY='your_key'")
            print()
            print("Option 3: Pass as argument:")
            print("  python Analyzer/audio_creation.py your_api_key")
            sys.exit(1)
    
    # Check for required files
    fixed_transcript = "processed/fixed_transcript.csv"
    original_audio = "processed/extracted/audio_latest.wav"
    
    # Find the most recent audio file
    audio_dir = "processed/extracted"
    if os.path.exists(audio_dir):
        audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]
        if audio_files:
            audio_files.sort()
            original_audio = os.path.join(audio_dir, audio_files[-1])
    
    if not os.path.exists(fixed_transcript):
        print(f"❌ Fixed transcript not found: {fixed_transcript}")
        print("Run main.py first to generate the cleaned transcript")
        sys.exit(1)
    
    if not os.path.exists(original_audio):
        print(f"❌ Original audio not found: {original_audio}")
        print("Run main.py first to extract audio")
        sys.exit(1)
    
    print(f"✅ Found files:")
    print(f"   Audio: {original_audio}")
    print(f"   Transcript: {fixed_transcript}")
    print()
    
    # Generate audio
    try:
        creator = AudioCreator(api_key)
        output = creator.clone_voice_and_generate(
            original_audio_path=original_audio,
            fixed_transcript_csv=fixed_transcript
        )
        
        print()
        print("=" * 60)
        print("✅ SUCCESS!")
        print("=" * 60)
        print(f"New audio file: {output}")
        print()
        print("🎧 Play the audio to hear the cleaned version!")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        print("Make sure:")
        print("  1. Your ElevenLabs API key is correct")
        print("  2. You have credits in your ElevenLabs account")
        print("  3. You have internet connection")