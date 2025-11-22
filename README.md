# Droid-hackathon
🎤 Speech Surgeon AI — Real-Time Speech Cleanup & Regeneration
Transform messy spoken audio into a clear, professional speech using OMI + Speechmatics + Convex + AI Voice.
🧩 Overview

Speech Surgeon AI is an intelligent speech-enhancement agent built for the AforeHacks hackathon.
It uses:

OMI to record raw speech

Speechmatics to precisely transcribe audio + detect timestamps + mark hesitation events

AI analysis to detect filler words, stutters, pacing issues, and clarity problems

AI rewriting to generate a cleaner, clearer version of the speech

AI text-to-speech to produce a polished version of the speech audio

Convex to store sessions, analysis, transcripts, metrics, and improvements

The result is a before-and-after transformation system that turns any messy recorded speech into a professional-quality spoken output.

This idea deeply integrates partner tools and demonstrates multi-step agent reasoning with a visually strong demo — perfect for scoring highly in this hackathon.

🎯 Why This Project?

Public speaking is hard. People struggle with:

“um”, “uh”, “like”, “so…”

stuttering / filler noises

speaking too fast

monotone delivery

unclear explanations

rambling or repeating themselves

Current editing tools clean audio — but don’t improve your actual speech.

Speech Surgeon AI fixes this.

🚀 End-to-End Workflow
1. Record Speech Using OMI

OMI listens to the user’s microphone and captures live speech audio.

Low-latency capture

Accurate segmentation

Simple UI (Record → Stop → Process)

OMI generates an audio file to send to Speechmatics.

2. Transcribe + Analyze with Speechmatics

Speechmatics provides:

transcript text

word-level timestamps

confidence scores

filler word detection (“uh”, “um”, “erm”, etc.)

hesitation markers

punctuation + sentence segmentation

This provides a highly accurate map of the user’s vocal delivery.

3. Speech Analysis Layer (Custom AI)

We run a series of analysis steps on the transcript + timestamps:

✔ Filler Words Detection

Counts & shows their exact positions in the timeline.

✔ Stutter / Hesitation Detection

Based on Speechmatics tags + repeated short patterns.

✔ Pacing Analysis

Words per minute
Variance
Speed spikes/slows
Long pause detection

✔ Clarity & Structure Assessment

Redundant sentences
Confusing sections
Run-on phrasing
Weak transitions

All of these metrics are stored in Convex.

4. Rewrite the Speech (AI Agent)

A multi-step agent takes the transcript + analysis and produces an improved version:

removes filler words

tightens pacing

reorganizes content

clarifies confusing sections

strengthens transitions

enhances tone and rhetorical flow

preserves original meaning

5. Regenerate Audio Using AI Voice (OpenAI or ElevenLabs)

The improved speech text is converted into clean, natural speech.

This produces:

even pacing

great clarity

no filler words

no stutters

clear emphasis

Optional:

clone user’s voice (premium)

use a professional-sounding voice

6. Convex: The Memory + Analytics Layer

Convex stores:

original transcript

improved transcript

filler timestamps

analysis metrics

audio URLs

before/after results

previous sessions (for improvement tracking)

Convex lets us display:

filler word heatmaps

pacing graphs

“before vs after” comparisons

clear improvement metrics

🖥️ User Interface
Upload/Record Page

Record speech (OMI)

Upload audio file (optional)

Show input waveform

“Process” button

Analysis Dashboard

filler word count

timeline stripes

pace graph (WPM over time)

stutter detection

clarity/structure flags

Rewrite Viewer

Side-by-side:

Original Transcript	Improved Transcript
messy version	clean version
Audio Player Comparison

Two audio players:

Before → original user audio
After → AI-regenerated improved audio

Export Options

download improved audio

download improved transcript

🏗️ Architecture Diagram
   ┌──────────────┐
   │     OMI       │
   │ (Record Mic)  │
   └───────┬───────┘
           │ audio file
           v
   ┌──────────────────────┐
   │    Speechmatics      │
   │ Transcription + NLP  │
   └───────┬──────────────┘
           │ transcript + timestamps
           v
   ┌────────────────────────────┐
   │    Speech Analysis Layer   │
   │ filler detection, pacing   │
   │ stutters, clarity tagging  │
   └───────┬────────────────────┘
           │ analysis summary
           v
   ┌────────────────────────────┐
   │    Rewrite AI Agent        │
   │ rewrites improved speech   │
   └───────┬────────────────────┘
           │ improved script
           v
   ┌────────────────────────────┐
   │   AI Voice Synthesis (TTS) │
   └───────┬────────────────────┘
           │ improved audio
           v
   ┌────────────────────────────┐
   │          Convex            │
   │ stores all data, logs,     │
   │ dashboards, and session    │
   └────────────────────────────┘

🗂️ Convex Data Model (Simplified)
// sessions.table
{
  id: string,
  userId: string,
  originalAudioUrl: string,
  improvedAudioUrl: string,
  transcript: string,
  improvedTranscript: string,
  createdAt: number
}

// analysis.table
{
  sessionId: string,
  fillerWords: number,
  pacing: { wpm: number, timeline: number[] },
  stutters: number,
  clarityIssues: string[],
  timeline: [
    { start: number, end: number, issue: string }
  ]
}