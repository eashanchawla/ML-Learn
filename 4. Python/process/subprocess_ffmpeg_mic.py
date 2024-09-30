"""
Write a Python script that uses subprocess to run ffmpeg to capture audio from a microphone.
Use a threading.Queue to store the audio data.

- Use subprocess.Popen() to start ffmpeg.
- Create a thread-safe queue to store audio data.
- Read from ffmpeg's stdout and put the data into the queue.
- Implement a simple consumer that reads from the queue and prints the data length.

Note: This is a complex task. You'll need to have ffmpeg installed and may need to adjust
      the ffmpeg command based on your system's audio setup.
"""

import subprocess
import threading
import queue

# Your code here
