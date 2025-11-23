from moviepy import VideoFileClip, concatenate_videoclips
import openai
from quickstart import generate_vid


def generation_pre(original_transcript, fixed_transcript):
    generation_time_stamps = [] # a list of tuples (start of phrase with filler, end of phrase)
    generation_phrases = [] 
    #for the phrase include the word before and after the filler
    #figure out the differece between generated fixed sentence and original, if there is more difference than jsut filler words, regenerate whole sentence if not just do before and after the filler word and get rid of it
    fillers = {
    "uh", "um", "er", "ah", "like", "you know", "i mean", "so", "well",
    "actually", "basically", "right", "okay", "ok", "hmm", "huh",
    "anyway", "literally", "just", "sort of", "kind of", "you see",
    "alright", "oh", "mm", "hmm", "umm", "ahh", "eh", "mhm"}#set of filler words
    fixed_index = 0
    word_time_stamps=[]#can we have the timestamps of each word

    words_i = 0
    for index, sentence in enumerate(original_transcript):
        for i, word in enumerate(sentence):
            if word in fillers:
                generation_time_stamps += [(word_time_stamps[0] if words_i == 0 else word_time_stamps[words_i-1],word_time_stamps[-1] if words_i == len(word_time_stamps)-1 else word_time_stamps[words_i+1])]
                generation_phrases += [[fixed_transcript[index][0 if i == 0 else i-1: i]]] #only need to do to i cause we got rid of the filler words in theory
                words_i += 1
            if word not in fillers and word != fixed_transcript[fixed_index]:
                generation_time_stamps += [(word_time_stamps[words_i-i], word_time_stamps[words_i+(len(sentence)-i)])]
                generation_phrases += [fixed_index[i][i+1]]
                words_i += len(sentence)-i
                break
    return (generation_time_stamps,generation_phrases)
    #figure out the differece between generated fixed sentence and original, if there is more difference than jsut filler words, regenerate whole sentence if not just do before and after the filler word and get rid of it

def seperate(generation_time_stamps, original_video_path):
    full_clip = VideoFileClip(original_video_path)

    clips = []

    last_end = 0
    # clip_index = 0
    # filler_index = 0
    index = 0
    for start, end in generation_time_stamps:
        if last_end < start:
            original_segment = full_clip.subclip(last_end, start)
            clip_file = f"clip{index}.mp4"
            original_segment.write_videofile(clip_file, codec="libx264")
            clips.append(clip_file)
            clip_index += 1

        filler_segment = full_clip.subclip(start, end)
        filler_file = f"filler{index}.mp4"
        filler_segment.write_videofile(filler_file, codec="libx264")
        clips.append(filler_file)
        filler_index += 1

        last_end = end

    if last_end < full_clip.duration:
        remaining_clip = full_clip.subclip(last_end, full_clip.duration)
        clip_file = f"clip{index}.mp4"
        remaining_clip.write_videofile(clip_file, codec="libx264")
        clips.append(clip_file)

    return clips

def combined(clips, phrases):
    for index, file in clips:
        if "filler" in file:
            audio=""#use phrases to generate the voice
            clips[index]= generate_vid(file,audio)
    final_video = concatenate_videoclips([VideoFileClip(f) for f in clips], method="compose")
    final_video.write_videofile("final_output.mp4", codec="libx264")
    return "final_output.mp4"
