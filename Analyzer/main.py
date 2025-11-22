"""
Main Pipeline: Video → Audio → Text → Clean → New Audio
Complete speech analysis pipeline with AI cleaning and audio generation
"""

import os
import sys
from audio_extraction import VideoProcessor
from text import AudioTranscriber
from speech_cleaner import SpeechCleaner
from audio_creation import AudioCreator

def main():
    """
    Main pipeline:
    1. Extract audio from video
    2. Transcribe audio to text
    3. Clean transcript with AI
    4. Display and save results
    """
    print("=" * 60)
    print("SPEECH SURGEON AI - COMPLETE PIPELINE")
    print("=" * 60)
    print()
    
    # Configuration - Try config.py first, then environment variables
    SPEECHMATICS_API_KEY = None
    GROQ_API_KEY = None
    ELEVENLABS_API_KEY = None
    
    try:
        from config import SPEECHMATICS_API_KEY as SM_KEY, GROQ_API_KEY as GQ_KEY
        SPEECHMATICS_API_KEY = SM_KEY
        GROQ_API_KEY = GQ_KEY
        try:
            from config import ELEVENLABS_API_KEY as EL_KEY
            ELEVENLABS_API_KEY = EL_KEY
        except ImportError:
            pass
    except ImportError:
        SPEECHMATICS_API_KEY = os.getenv('SPEECHMATICS_API_KEY')
        GROQ_API_KEY = os.getenv('GROQ_API_KEY')
        ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    
    # Check for required API keys
    if not SPEECHMATICS_API_KEY:
        print("❌ SPEECHMATICS_API_KEY not set!")
        print()
        print("Option 1: Create Analyzer/config.py with:")
        print("  SPEECHMATICS_API_KEY = 'your_key'")
        print("  GROQ_API_KEY = 'your_key'")
        print()
        print("Option 2: Set environment variable:")
        print("  export SPEECHMATICS_API_KEY='your_key'")
        sys.exit(1)
    
    if not GROQ_API_KEY:
        print("⚠️ GROQ_API_KEY not set - AI cleaning will be skipped")
        print()
    
    # Step 0: Automatically find video file (.mp4 or .mov)
    if len(sys.argv) > 1:
        # Use command line argument if provided
        video_path = sys.argv[1]
    else:
        # Automatically find .mp4 or .mov file in project root
        video_files = [f for f in os.listdir('.') if f.endswith(('.mp4', '.mov', '.MOV', '.MP4'))]
        
        if not video_files:
            print(f"❌ No video files (.mp4 or .mov) found in project root")
            print()
            print("Please:")
            print("  1. Place a video file in the project root, OR")
            print("  2. Run: python Analyzer/main.py path/to/video.mp4")
            sys.exit(1)
        
        # Use the first video file found
        video_path = video_files[0]
        
        if len(video_files) > 1:
            print(f"📹 Multiple videos found: {', '.join(video_files)}")
            print(f"📹 Using: {video_path}")
            print()
    
    # Check if video exists
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        sys.exit(1)
    
    # Convert .mov to .mp4 if needed
    if video_path.lower().endswith('.mov'):
        print(f"📹 Converting .mov to .mp4...")
        import subprocess
        mp4_path = video_path.rsplit('.', 1)[0] + '.mp4'
        
        try:
            subprocess.run([
                'ffmpeg', '-i', video_path,
                '-vcodec', 'copy',
                '-acodec', 'copy',
                '-y',
                mp4_path
            ], check=True, capture_output=True)
            
            print(f"✅ Converted to: {mp4_path}")
            video_path = mp4_path
        except Exception as e:
            print(f"⚠️ Conversion failed, using original .mov file")
            print(f"   Error: {str(e)}")
        print()
    
    print(f"📹 Video file: {video_path}")
    print()
    
    try:
        # Step 1: Extract Audio from Video
        print("-" * 60)
        print("STEP 1: EXTRACTING AUDIO FROM VIDEO")
        print("-" * 60)
        
        video_processor = VideoProcessor()
        audio_path = video_processor.extract_audio(video_path)
        
        print(f"✅ Audio extracted successfully!")
        print(f"   Audio file: {audio_path}")
        print()
        
        # Step 2: Transcribe Audio to Text
        print("-" * 60)
        print("STEP 2: TRANSCRIBING AUDIO TO TEXT")
        print("-" * 60)
        
        transcriber = AudioTranscriber(SPEECHMATICS_API_KEY)
        result = transcriber.transcribe(audio_path)
        
        print(f"✅ Transcription complete!")
        print()
        
        # Step 3: Display Results
        print("=" * 60)
        print("RESULTS")
        print("=" * 60)
        print()
        
        print("📊 STATISTICS:")
        print(f"   Word count: {result['metadata']['word_count']}")
        print(f"   Duration: {result['metadata']['duration']:.2f} seconds")
        print()
        
        print("📝 TRANSCRIPT:")
        print("-" * 60)
        print(result['transcript'])
        print("-" * 60)
        print()
        
        # Step 4: Save Results (JSON and CSV)
        output_json = "processed/transcript.json"
        output_csv = "processed/transcript.csv"
        
        # Save JSON
        transcriber.save_transcript(result, output_json)
        
        # Save CSV with full transcript text
        import csv
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['transcript'])
            writer.writerow([result['transcript']])
        
        print(f"Transcript CSV saved to: {output_csv}")
        print()
        
        # Step 5: Clean Transcript with AI (if Groq API key available)
        cleaned_transcript = None
        output_fixed_csv = "processed/fixed_transcript.csv"
        
        if GROQ_API_KEY:
            print("-" * 60)
            print("STEP 5: CLEANING TRANSCRIPT WITH AI")
            print("-" * 60)
            
            try:
                cleaner = SpeechCleaner(GROQ_API_KEY)
                cleaned_transcript = cleaner.improve_transcript(result['transcript'])
                
                print()
                print("📝 CLEANED TRANSCRIPT:")
                print("-" * 60)
                print(cleaned_transcript)
                print("-" * 60)
                print()
                
                # Save cleaned transcript to CSV
                cleaner.save_cleaned_csv(cleaned_transcript, output_fixed_csv)
                print()
                
            except Exception as e:
                print(f"⚠️ Failed to clean transcript: {str(e)}")
                print("   (Original transcript is still available)")
                print()
        else:
            print("-" * 60)
            print("⚠️ Groq API key not set - skipping AI cleaning")
            print("   To enable: export GROQ_API_KEY='your_api_key_here'")
            print("-" * 60)
            print()
        
        # Step 6: Generate New Audio (if ElevenLabs API key available and transcript was cleaned)
        output_improved_audio = None
        
        if ELEVENLABS_API_KEY and cleaned_transcript:
            print("-" * 60)
            print("STEP 6: GENERATING NEW AUDIO WITH CLEANED SPEECH")
            print("-" * 60)
            
            try:
                audio_creator = AudioCreator(ELEVENLABS_API_KEY)
                output_improved_audio = audio_creator.clone_voice_and_generate(
                    original_audio_path=audio_path,
                    fixed_transcript_csv=output_fixed_csv,
                    output_path="processed/improved_audio.mp3"
                )
                
                print()
                
            except Exception as e:
                print(f"⚠️ Failed to generate new audio: {str(e)}")
                print("   (Original and cleaned transcripts are still available)")
                print()
        elif not ELEVENLABS_API_KEY:
            print("-" * 60)
            print("⚠️ ElevenLabs API key not set - skipping audio generation")
            print("   To enable: Add ELEVENLABS_API_KEY to config.py")
            print("-" * 60)
            print()
        elif not cleaned_transcript:
            print("-" * 60)
            print("⚠️ No cleaned transcript available - skipping audio generation")
            print("-" * 60)
            print()
        
        print()
        print("=" * 60)
        print("✅ PIPELINE COMPLETE!")
        print("=" * 60)
        print()
        print(f"📁 Files created:")
        print(f"   Video: {video_path}")
        print(f"   Audio: {audio_path}")
        print(f"   Transcript JSON: {output_json}")
        print(f"   Transcript CSV: {output_csv}")
        if cleaned_transcript:
            print(f"   Fixed Transcript CSV: {output_fixed_csv}")
        print()
        print("🎉 Your video has been successfully processed!")
        
        # Return paths for future use
        return {
            'video_path': video_path,
            'audio_path': audio_path,
            'transcript_json': output_json,
            'transcript_csv': output_csv,
            'transcript_text': result['transcript'],
            'fixed_transcript_csv': output_fixed_csv if cleaned_transcript else None,
            'cleaned_transcript': cleaned_transcript
        }
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR IN PIPELINE")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()