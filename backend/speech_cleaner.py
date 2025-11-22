import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def improve_transcript(raw_transcript: str) -> str:
    prompt = f"""
You are a speech improvement assistant.

Clean this transcript by:
- Removing filler words (um, uh, like, you know)
- Removing stutters and repeated words
- Fixing grammar and punctuation
- Improving clarity and flow
- Keeping the original meaning
- Not adding new ideas

Transcript:
\"\"\"{raw_transcript}\"\"\"

Return only the improved transcript.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # 100% supported, NOT decommissioned
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=600
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    sample = "One Hi my name is Dave Lucero Wala Um I want to introduce you to our northeastern Californian community Um um my pronouns are uh he him Uh And I want to um highlight some features of student life here in the Bay areacl"
    print("RAW:", sample)
    print("CLEAN:", improve_transcript(sample))
