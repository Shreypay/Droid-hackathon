"""
Audio to Text Transcription using Speechmatics
Converts audio files to text with detailed analysis
"""

import os
import json
import requests

class AudioTranscriber:
    """Transcribe audio files using Speechmatics"""
    
    def __init__(self, api_key: str):
        """
        Initialize the transcriber
        
        Args:
            api_key: Your Speechmatics API key
        """
        self.api_key = api_key
        self.base_url = "https://asr.api.speechmatics.com/v2"
    
    def transcribe(self, audio_path: str, language: str = "en") -> dict:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to the audio file (.wav)
            language: Language code (default: "en" for English)
            
        Returns:
            Dictionary containing:
                - transcript: Full text transcript
                - words: List of words with timestamps
                - metadata: Additional info (confidence, duration, etc.)
        """
        # Check if audio file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"Transcribing audio: {audio_path}")
        
        # Step 1: Submit the job
        job_config = {
            "type": "transcription",
            "transcription_config": {
                "language": language
            }
        }
        
        try:
            # Open and send the audio file
            with open(audio_path, 'rb') as audio_file:
                files = {
                    'data_file': (os.path.basename(audio_path), audio_file, 'audio/wav'),
                    'config': (None, json.dumps(job_config), 'application/json')
                }
                
                headers = {
                    'Authorization': f'Bearer {self.api_key}'
                }
                
                print("Submitting transcription job...")
                response = requests.post(
                    f"{self.base_url}/jobs",
                    headers=headers,
                    files=files
                )
                
                if response.status_code != 201:
                    raise Exception(f"Failed to submit job: {response.status_code} - {response.text}")
                
                job_id = response.json()['id']
                print(f"Job submitted. Job ID: {job_id}")
                print("Waiting for transcription to complete...")
            
            # Step 2: Poll for job completion
            import time
            while True:
                status_response = requests.get(
                    f"{self.base_url}/jobs/{job_id}",
                    headers=headers
                )
                
                if status_response.status_code != 200:
                    raise Exception(f"Failed to get job status: {status_response.text}")
                
                job_status = status_response.json()['job']['status']
                
                if job_status == 'done':
                    print("✅ Transcription complete!")
                    break
                elif job_status == 'rejected':
                    raise Exception("Job was rejected by Speechmatics")
                
                print(f"Status: {job_status}...")
                time.sleep(2)
            
            # Step 3: Get the transcript
            transcript_response = requests.get(
                f"{self.base_url}/jobs/{job_id}/transcript",
                headers=headers,
                params={'format': 'json-v2'}
            )
            
            if transcript_response.status_code != 200:
                raise Exception(f"Failed to get transcript: {transcript_response.text}")
            
            transcript_data = transcript_response.json()
            
            # Parse the results
            result = self._parse_transcript(transcript_data)
            return result
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def _parse_transcript(self, transcript_data: dict) -> dict:
        """
        Parse Speechmatics response into organized format
        
        Args:
            transcript_data: Raw response from Speechmatics
            
        Returns:
            Organized dictionary with transcript and analysis data
        """
        # Extract full transcript text
        results = transcript_data.get('results', [])
        full_transcript = ""
        words_list = []
        
        for result in results:
            if result.get('type') == 'word':
                word_data = {
                    'word': result.get('alternatives', [{}])[0].get('content', ''),
                    'start': result.get('start_time', 0),
                    'end': result.get('end_time', 0),
                    'confidence': result.get('alternatives', [{}])[0].get('confidence', 0)
                }
                words_list.append(word_data)
                full_transcript += word_data['word'] + " "
        
        # Get metadata
        metadata = transcript_data.get('metadata', {})
        
        return {
            'transcript': full_transcript.strip(),
            'words': words_list,
            'metadata': {
                'duration': metadata.get('transcription_time', 0),
                'word_count': len(words_list),
                'language': 'en'
            },
            'raw_data': transcript_data  # Keep full response for detailed analysis
        }
    
    def save_transcript(self, result: dict, output_path: str):
        """
        Save transcript result to JSON file
        
        Args:
            result: Transcript result dictionary
            output_path: Path to save JSON file
        """
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Transcript saved to: {output_path}")


# TEST CODE
if __name__ == "__main__":
    import sys
    
    print("=" * 50)
    print("AUDIO TO TEXT TRANSCRIPTION TEST")
    print("=" * 50)
    print()
    
    # Get API key from environment or command line
    api_key = os.getenv('SPEECHMATICS_API_KEY')
    
    if not api_key:
        # Check if passed as argument
        if len(sys.argv) > 1:
            api_key = sys.argv[1]
            print(f"✅ Using API key from argument")
        else:
            # Use hardcoded API key for testing
            api_key = "V7jlalVsvvwH9NewBt1qaknMWn5yLaiV"
            print(f"✅ Using hardcoded API key")
    
    if not api_key:
        print("❌ Speechmatics API key not found!")
        sys.exit(1)
    
    # Look for audio file in processed/extracted
    audio_dir = "processed/extracted"
    
    if not os.path.exists(audio_dir):
        print(f"❌ Directory not found: {audio_dir}")
        print("Run audio_extraction.py first to extract audio from video")
        sys.exit(1)
    
    # Find the most recent audio file
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]
    
    if not audio_files:
        print(f"❌ No audio files found in {audio_dir}")
        print("Run audio_extraction.py first to extract audio from video")
        sys.exit(1)
    
    # Get the most recent file
    audio_files.sort()
    audio_path = os.path.join(audio_dir, audio_files[-1])
    
    print(f"✅ Found audio file: {audio_path}")
    print()
    
    # Transcribe
    try:
        transcriber = AudioTranscriber(api_key)
        result = transcriber.transcribe(audio_path)
        
        print()
        print("=" * 50)
        print("✅ TRANSCRIPTION SUCCESS!")
        print("=" * 50)
        print()
        print("TRANSCRIPT:")
        print("-" * 50)
        print(result['transcript'])
        print("-" * 50)
        print()
        print(f"Word count: {result['metadata']['word_count']}")
        print(f"Duration: {result['metadata']['duration']:.2f} seconds")
        print()
        
        # Save to file
        output_file = "processed/transcript.json"
        transcriber.save_transcript(result, output_file)
        print(f"\nFull results saved to: {output_file}")
        
    except Exception as e:
        print()
        print("=" * 50)
        print("❌ ERROR")
        print("=" * 50)
        print(f"Error: {str(e)}")
        print()
        print("Make sure:")
        print("  1. Your API key is correct")
        print("  2. You have internet connection")
        print("  3. Your Speechmatics account is active")