"""
Speech Cleaner using Groq AI
Removes fillers, stutters, and improves clarity
"""

import os
from groq import Groq

class SpeechCleaner:
    """Clean and improve transcripts using AI"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize speech cleaner
        
        Args:
            api_key: Groq API key (or uses GROQ_API_KEY env var)
        """
        if api_key is None:
            api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError("Groq API key not provided")
        
        self.client = Groq(api_key=api_key)
    
    def improve_transcript(self, raw_transcript: str) -> str:
        """
        Clean and improve a transcript
        
        Args:
            raw_transcript: The raw transcript text
            
        Returns:
            Cleaned and improved transcript
        """
        prompt = f"""
You are a speech improvement assistant.

Clean this transcript by:
- Removing filler words (um, uh, like, you know, so, basically, actually)
- Removing stutters and repeated words
- Fixing grammar and punctuation
- Improving clarity and flow
- Keeping the original meaning and tone
- Not adding new ideas or information

Transcript:
\"\"\"{raw_transcript}\"\"\"

Return ONLY the improved transcript with no preamble or explanation.
"""

        try:
            print("🤖 Cleaning transcript with AI...")
            
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2000
            )
            
            cleaned = response.choices[0].message.content.strip()
            
            print("✅ Transcript cleaned!")
            return cleaned
            
        except Exception as e:
            raise Exception(f"Failed to clean transcript: {str(e)}")
    
    def save_cleaned_csv(self, cleaned_transcript: str, output_path: str):
        """
        Save cleaned transcript to CSV
        
        Args:
            cleaned_transcript: The cleaned transcript text
            output_path: Path to save CSV file
        """
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['fixed_transcript'])
            writer.writerow([cleaned_transcript])
        
        print(f"Fixed transcript CSV saved to: {output_path}")


# TEST CODE
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("SPEECH CLEANER TEST")
    print("=" * 60)
    print()
    
    # Get API key
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        if len(sys.argv) > 1:
            api_key = sys.argv[1]
            print("✅ Using API key from argument")
        else:
            print("❌ Groq API key not found!")
            print()
            print("Set your API key:")
            print("  export GROQ_API_KEY='your_api_key_here'")
            print()
            print("Or pass it as argument:")
            print("  python Analyzer/speech_cleaner.py your_api_key_here")
            sys.exit(1)
    
    # Test with sample
    sample = "One Hi my name is Dave Lucero Wala Um I want to introduce you to our northeastern Californian community Um um my pronouns are uh he him Uh And I want to um highlight some features of student life here in the Bay areacl"
    
    print("RAW TRANSCRIPT:")
    print("-" * 60)
    print(sample)
    print("-" * 60)
    print()
    
    try:
        cleaner = SpeechCleaner(api_key)
        cleaned = cleaner.improve_transcript(sample)
        
        print()
        print("CLEANED TRANSCRIPT:")
        print("-" * 60)
        print(cleaned)
        print("-" * 60)
        print()
        
        # Save to CSV
        output_file = "processed/fixed_transcript.csv"
        cleaner.save_cleaned_csv(cleaned, output_file)
        print()
        print(f"✅ Saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")