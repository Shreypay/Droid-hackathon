# quickstart.py
import time
from sync import Sync
from sync.common import Audio, GenerationOptions, Video
from sync.core.api_error import ApiError

# ---------- UPDATE API KEY ----------
# Replace with your Sync.so API key
api_key = "sk-JAP3fotwQ8KAKZ4iKYf_yg.VGFw-aMESDWTPMz0k_0Dh39Iui3wUIJU" 

def generate_vid(audio_url):

    video_url = "https://drive.google.com/file/d/1OVjzmRHNLRKp-q0X6I5kWlcCI2LcYHoj/view?usp=sharing"
    audio_url = "https://drive.google.com/file/d/1-5E2Zo2YYXzm3eJgo7o2d83kJMDgQ59A/view?usp=sharing"

    client = Sync(
        base_url="https://api.sync.so", 
        api_key=api_key
    ).generations

    print("Starting lip sync generation job...")

    try:
        response = client.create(
            input=[Video(url=video_url),Audio(url=audio_url)],
            model="lipsync-2",
            options=GenerationOptions(sync_mode="cut_off"),
        )
    except ApiError as e:
        print(f'create generation request failed with status code {e.status_code} and error {e.body}')
        exit()

    job_id = response.id
    print(f"Generation submitted successfully, job id: {job_id}")

    generation = client.get(job_id)
    status = generation.status
    while status not in ['COMPLETED', 'FAILED']:
        print('polling status for generation', job_id)
        time.sleep(10)
        generation = client.get(job_id)
        status = generation.status

    if status == 'COMPLETED':
        print('generation', job_id, 'completed successfully, output url:', generation.output_url)
    else:
        print('generation', job_id, 'failed')
    return generation.output_url

generate_vid("")