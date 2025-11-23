import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  sessions: defineTable({
    userId: v.string(),
    timestamp: v.number(),
    
    // Transcript data
    transcriptText: v.string(),
    cleanedText: v.string(),
    
    // Metadata
    metadata: v.object({
      word_count: v.number(),
      duration: v.number(),
      language: v.string(),
    }),
    
    // Files (base64 encoded)
    files: v.object({
      video: v.optional(v.string()),
      video_name: v.optional(v.string()),
      original_audio: v.optional(v.string()),
      original_audio_name: v.optional(v.string()),
      transcript_json: v.optional(v.string()),
      transcript_csv: v.optional(v.string()),
      fixed_transcript_csv: v.optional(v.string()),
      improved_audio_mp3: v.optional(v.string()),
      improved_audio_wav: v.optional(v.string()),
      improved_audio_name: v.optional(v.string()),
    }),
  })
    .index("by_user", ["userId"])
    .index("by_timestamp", ["timestamp"]),
});