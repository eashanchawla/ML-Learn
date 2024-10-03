"""
Assignment: Multithreaded File Processor

Implement a multithreaded file processing system that:

1. Reads multiple text files from a directory
2. Processes each file in a separate thread (e.g., count words, find specific patterns)
3. Aggregates the results from all threads
4. Writes a summary report to a new file

Requirements:
- Use the threading module to create and manage threads
- Implement a thread-safe mechanism for aggregating results
- Handle potential race conditions and deadlocks
- Provide progress updates during processing

Bonus:
- Implement a thread pool to limit the number of concurrent threads
- Add support for processing different file types (e.g., CSV, JSON)
"""

# Your code here
