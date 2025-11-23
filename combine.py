from video import generation_pre,seperate,combined
from speech_cleaner import improve_transcript
from processing_video import video_processing
#get video
#generate transcript
video = "test.mp4"
_,_,_,_,raw_transcript,_,fixed_transcript =video_processing(video)
generation_time_stamps,generation_phrases = generation_pre(raw_transcript, fixed_transcript)
print(generation_phrases)
clips = seperate(generation_time_stamps, video)
# final = combined(clips,generation_phrases)



