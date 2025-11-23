
// quickstart.ts
import { SyncClient, SyncError } from "@sync.so/sdk";

// ---------- UPDATE API KEY ----------
// Replace with your Sync.so API key
const apiKey = "sk-JAP3fotwQ8KAKZ4iKYf_yg.VGFw-aMESDWTPMz0k_0Dh39Iui3wUIJU";

// ----------[OPTIONAL] UPDATE INPUT VIDEO AND AUDIO URL ----------
// URL to your source video
const videoUrl = "https://drive.google.com/file/d/11yawaobLN53grrGnLi6h14M1JpXLxvkx/view?usp=sharing"
// URL to your audio file
const audioUrl =  "https://drive.google.com/file/d/1TEFhcdEYFpA57xjew025sdqB175xoLu-/view?usp=sharing"
// ----------------------------------------

const client = new SyncClient({ apiKey });

async function main() {
    console.log("Starting lip sync generation job...");

    let jobId: string;
    try {
        const response = await client.generations.create({
            input: [
                {
                    type: "video",
                    url: videoUrl,
                },
                {
                    type: "audio",
                    url: audioUrl,
                },
            ],
            model: "lipsync-2",
            options: {
                sync_mode: "cut_off",
            },
            outputFileName: "quickstart"
        });
        jobId = response.id;
        console.log(`Generation submitted successfully, job id: ${jobId}`);
    } catch (err) {
        if (err instanceof SyncError) {
            console.error(`create generation request failed with status code ${err.statusCode} and error ${JSON.stringify(err.body)}`);
        } else {
            console.error('An unexpected error occurred:', err);
        }
        return;
    }

    let generation;
    let status;
    while (status !== 'COMPLETED' && status !== 'FAILED') {
        console.log(`polling status for generation ${jobId}...`);
        try {
            await new Promise(resolve => setTimeout(resolve, 10000));
            generation = await client.generations.get(jobId);
            status = generation.status;
        } catch (err) {
            if (err instanceof SyncError) {
                console.error(`polling failed with status code ${err.statusCode} and error ${JSON.stringify(err.body)}`);
            } else {
                console.error('An unexpected error occurred during polling:', err);
            }
            status = 'FAILED';
        }
    }

    if (status === 'COMPLETED') {
        console.log(`generation ${jobId} completed successfully, output url: ${generation?.outputUrl}`);
    } else {
        console.log(`generation ${jobId} failed`);
    }
}

main();