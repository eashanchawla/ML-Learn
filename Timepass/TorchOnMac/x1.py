import argparse
import os
import numpy as np
import torch
import subprocess
import threading
import logging
import collections
import asyncio
import webrtcvad

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="small", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the English model.")
    parser.add_argument("--energy_threshold", default=1000,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=3,
                        help="How real-time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=3,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)
    args = parser.parse_args()

    phrase_time = None
    data_queue = Queue()

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.backends.mps.is_available() else torch.float32
    model_id = "distil-whisper/distil-small.en"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, use_safetensors=True, low_cpu_mem_usage=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    audio_model = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device
    )

    logger.info('Model loading done')
    record_timeout = args.record_timeout
    phrase_timeout = args.phrase_timeout

    transcription = ['']

    # Define overlapping and buffering parameters
    overlap_timeout = 1.0  # 1 second overlap
    chunk_size = int(16000 * record_timeout * 2)  # 16kHz * seconds * 2 bytes
    overlap_size = int(16000 * overlap_timeout * 2)

    # ffmpeg command to capture audio from the default microphone on macOS (avfoundation)
    ffmpeg_command = [
        'ffmpeg',
        '-f', 'avfoundation',     # Input device for macOS
        '-i', ':0',               # Default microphone
        '-ac', '1',               # Single audio channel (mono)
        '-ar', '16000',           # Audio sampling rate: 16kHz
        '-f', 'wav',              # Output format: WAV
        '-hide_banner',           # Hide banner info
        '-loglevel', 'error',     # Suppress unnecessary output
        'pipe:1'                  # Output to stdout (pipe)
    ]

    # Create a subprocess to run ffmpeg for continuous audio capture
    try:
        ffmpeg_process = subprocess.Popen(
            ffmpeg_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # Capture stderr for debugging
            bufsize=10**8
        )
    except Exception as e:
        logger.error(f"Failed to start FFmpeg subprocess: {e}")
        return

    logger.info("FFmpeg subprocess started.")

    def read_audio_with_overlap(ffmpeg_process, queue, chunk_size, overlap_size):
        buffer = b''
        while True:
            try:
                audio_chunk = ffmpeg_process.stdout.read(chunk_size)
                if len(audio_chunk) == 0:
                    logger.warning("No more audio data received from FFmpeg.")
                    break
                combined_chunk = buffer + audio_chunk
                queue.put(combined_chunk)
                buffer = audio_chunk[-overlap_size:]  # Update buffer with overlap
            except Exception as e:
                logger.error(f"Error reading audio from FFmpeg: {e}")
                break

    # Start reading audio with overlapping windows in a separate thread
    audio_thread = threading.Thread(
        target=read_audio_with_overlap, 
        args=(ffmpeg_process, data_queue, chunk_size, overlap_size), 
        daemon=True
    )
    audio_thread.start()

    logger.info("Audio reading thread with overlapping windows started.\n")

    # Initialize VAD
    vad = webrtcvad.Vad(2)  # Aggressiveness mode (0-3)

    def transcribe_audio(queue, audio_model, transcription, vad, phrase_timeout):
        buffer_audio = b''
        phrase_time = None
        while True:
            try:
                if not queue.empty():
                    audio_data = queue.get()
                    # VAD processing
                    frames = frame_generator(30, audio_data, 16000)
                    frames = list(frames)
                    segments = vad_collector(16000, 30, 300, vad, frames)
                    for segment in segments:
                        audio_np = np.frombuffer(segment, dtype=np.int16).astype(np.float32) / 32768.0
                        audio_np = np.reshape(audio_np, (-1,))
                        result = audio_model(audio_np)
                        text = result['text'].strip()
                        if phrase_time and datetime.utcnow() - phrase_time > timedelta(seconds=phrase_timeout):
                            transcription.append(text)
                        else:
                            transcription[-1] = text
                        phrase_time = datetime.utcnow()

                        # Clear the console to reprint the updated transcription.
                        os.system('cls' if os.name == 'nt' else 'clear')
                        for line in transcription:
                            print(line)
                        # Flush stdout
                        print('', end='', flush=True)
                else:
                    sleep(0.25)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"An error occurred during transcription: {e}")
                break

    # Helper functions for VAD
    from collections import deque

    class Frame:
        """Represents a "frame" of audio data."""
        def __init__(self, bytes, timestamp, duration):
            self.bytes = bytes
            self.timestamp = timestamp
            self.duration = duration

    def frame_generator(frame_duration_ms, audio, sample_rate):
        n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)  # 16-bit audio
        offset = 0
        timestamp = 0.0
        duration = (float(n) / (2 * sample_rate))
        while offset + n <= len(audio):
            yield Frame(audio[offset:offset + n], timestamp, duration)
            timestamp += duration
            offset += n

    def vad_collector(sample_rate, frame_duration_ms, padding_duration_ms, vad, frames):
        """Filters out non-voiced audio frames."""
        num_padding_frames = int(padding_duration_ms / frame_duration_ms)
        ring_buffer = deque(maxlen=num_padding_frames)
        triggered = False

        voiced_frames = []
        for frame in frames:
            is_speech = vad.is_speech(frame.bytes, sample_rate)
            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                if num_voiced > 0.9 * ring_buffer.maxlen:
                    triggered = True
                    voiced_frames.extend([f.bytes for f, s in ring_buffer])
                    ring_buffer.clear()
            else:
                voiced_frames.append(frame.bytes)
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                if num_unvoiced > 0.9 * ring_buffer.maxlen:
                    triggered = False
                    yield b''.join(voiced_frames)
                    ring_buffer.clear()
                    voiced_frames = []
        if voiced_frames:
            yield b''.join(voiced_frames)

    # Start transcription in a separate thread
    transcribe_thread = threading.Thread(
        target=transcribe_audio,
        args=(data_queue, audio_model, transcription, vad, phrase_timeout),
        daemon=True
    )
    transcribe_thread.start()

    logger.info("Transcription thread started.\n")

    try:
        while True:
            sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Exiting...")

    # Terminate FFmpeg subprocess
    ffmpeg_process.terminate()
    ffmpeg_process.wait()

    print("\n\nTranscription:")
    for line in transcription:
        print(line)

if __name__ == "__main__":
    main()
