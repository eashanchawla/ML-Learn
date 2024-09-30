import sys
from transformers.pipelines.audio_utils import ffmpeg_microphone_live
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
device = "mps" if torch.backends.mps.is_available() else "cpu"

transcriber = pipeline(
    "automatic-speech-recognition", model="openai/whisper-base.en", device=device
)

def transcribe(chunk_length_s=5.0, stream_chunk_s=1.0):
    sampling_rate = transcriber.feature_extractor.sampling_rate

    mic = ffmpeg_microphone_live(
        sampling_rate=sampling_rate,
        chunk_length_s=chunk_length_s,
        stream_chunk_s=stream_chunk_s,
    )

    print("Start speaking...")
    for item in transcriber(mic, generate_kwargs={"max_new_tokens": 128}):
        # Clear the line and return the cursor to the start
        sys.stdout.write("\r\033[K")
        # Write the new transcribed text
        sys.stdout.write(item["text"])
        # Ensure the text is displayed immediately
        sys.stdout.flush()
        
        # Optional: Simulate processing time
        # time.sleep(0.1)
        
        # Terminate after the first complete transcription chunk
        if not item["partial"][0]:
            break
        # if not item.get("is_partial", True):
        #     break

    print()  # Move to the next line after transcription is complete
    return item["text"]


transcribe(60, 5)
