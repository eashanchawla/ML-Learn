import sys
from transformers.pipelines.audio_utils import ffmpeg_microphone_live
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

device = "mps" if torch.backends.mps.is_available() else "cpu"
torch_dtype = torch.float16 if torch.backends.mps.is_available() else torch.float32
model_id = "distil-whisper/distil-medium.en"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, use_safetensors=True, low_cpu_mem_usage=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

transcriber = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device
)

# def transcribe(chunk_length_s=60.0, stream_chunk_s=10.0):
#     sampling_rate = transcriber.feature_extractor.sampling_rate

#     mic = ffmpeg_microphone_live(
#         sampling_rate=sampling_rate,
#         chunk_length_s=chunk_length_s,
#         stream_chunk_s=stream_chunk_s,
#     )

#     print("Start speaking...")
#     prev_text = ""
#     final_text = ""

#     for item in transcriber(mic, generate_kwargs={"max_new_tokens": 128}):
#         sys.stdout.write("\033[K")
#         current_text = item["text"]

#         # Only update when the text changes to avoid redundant printing
#         if current_text != prev_text:
#             print('new:', current_text, end="\r")
#             prev_text = current_text

#         # If the transcription is not partial anymore, append it to final text
#         if not item["partial"]:
#             final_text += " " + current_text  # Capture final chunk
        
#         # Continue looping and capturing speech without breaking

#     return final_text

fin=list()
def transcribe(chunk_length_s=15.0, stream_chunk_s=1.0):
    sampling_rate = transcriber.feature_extractor.sampling_rate

    mic = ffmpeg_microphone_live(
        sampling_rate=sampling_rate,
        chunk_length_s=chunk_length_s,
        stream_chunk_s=stream_chunk_s,
    )

    print("Start speaking...")
    for item in transcriber(mic, generate_kwargs={"max_new_tokens": 128}):
        sys.stdout.write("\033[K")
        print('new:', item["text"], end="\r")
        fin.append(item)
        if not item["partial"][0]:
            break

    return item["text"]

if __name__ == '__main__':
    transcribe(300, 30)
    print('End')
    print(fin)