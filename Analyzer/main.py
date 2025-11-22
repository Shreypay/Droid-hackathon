"""
Main Pipeline: Video → Audio → Text
Complete speech analysis pipeline
"""

import os
import sys
from audio_extraction import VideoProcessor
from text import AudioTranscriber

def main():
    """
    Main pipeline:
    1. Extract audio from video
    2. Transcribe audio to text
    3. Display and save results
    """
    print("=" * 60)
    print("SPEECH SURGEON AI - COMPLETE PIPELINE")
    print("=" * 60)
    print()
    
    # Configuration
    SPEECHMATICS_API_KEY = "V7jlalVsvvwH9NewBt1qaknMWn5yLaiV"
    
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
        print("=" * 60)
        print("✅ PIPELINE COMPLETE!")
        print("=" * 60)
        print()
        print(f"📁 Files created:")
        print(f"   Video: {video_path}")
        print(f"   Audio: {audio_path}")
        print(f"   Transcript JSON: {output_json}")
        print(f"   Transcript CSV: {output_csv}")
        print()
        print("🎉 Your video has been successfully transcribed!")
        
        # Return paths for Convex storage
        return {
            'video_path': video_path,
            'audio_path': audio_path,
            'transcript_json': output_json,
            'transcript_csv': output_csv,
            'transcript_text': result['transcript']
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