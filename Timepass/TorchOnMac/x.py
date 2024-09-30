import sys
import time
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset

# Determine the device (MPS for Apple Silicon, otherwise CPU)
device = "mps" if torch.backends.mps.is_available() else "cpu"
torch_dtype = torch.float16 if torch.backends.mps.is_available() else torch.float32

# Track the time to load the model
start_time = time.time()

# Load the model and processor
model_id = "distil-whisper/distil-medium.en"
# model = AutoModelForSpeechSeq2Seq.from_pretrained(
#     model_id, torch_dtype=torch_dtype, use_safetensors=True, low_cpu_mem_usage=True
# )
# model.to(device)

# processor = AutoProcessor.from_pretrained(model_id)

# pipe = pipeline(
#     "automatic-speech-recognition",
#     model=model,
#     tokenizer=processor.tokenizer,
#     feature_extractor=processor.feature_extractor,
#     torch_dtype=torch_dtype,
#     device=device
# )

# Time taken to load the model
model_load_time = time.time() - start_time
print(f"Time taken to load the model: {model_load_time:.2f} seconds")

# Load the dataset
dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")

# Iterate over the dataset and transcribe each audio sample, while tracking time
for i in range(len(dataset)):
    sample = dataset[i]["audio"]
    print(type(sample))
    # print(sample['path'])
    print(sample['array'].shape)
    print(sample['sampling_rate'])
    # # Track the time taken for transcription
    # start_transcription_time = time.time()
    # result = pipe(sample)
    # transcription_time = time.time() - start_transcription_time

    # print(f"Transcription {i+1}: {result['text']}")
    # print(f"Time taken for transcription {i+1}: {transcription_time:.2f} seconds")
    break