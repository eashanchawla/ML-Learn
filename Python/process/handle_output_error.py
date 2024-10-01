"""
This script demonstrates how to handle both output and error streams from a subprocess.

Assignment:
1. Use the subprocess module to execute the command 'ls -l /nonexistent_directory'.
2. Capture both stdout and stderr from this command.
3. Print both the captured output and error messages.

Key concepts:
- Using subprocess.run() with arguments to capture both stdout and stderr
- Handling command execution that is expected to fail
- Differentiating between standard output and error output

Note: This command is designed to fail, as it tries to list a non-existent directory.
"""

# Your code here
import subprocess

output = subprocess.run(["ls", "-l", "/nonexistent_directory"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
if output.returncode != 0:
    print("Error occurred")
    print(output.stderr.decode())
else:
    print(output.stdout.decode())