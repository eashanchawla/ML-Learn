"""
Assignment: Global Interpreter Lock (GIL) Demonstration

Create a program that demonstrates the effects of the Global Interpreter Lock on CPU-bound tasks:

1. Implement a CPU-intensive function (e.g., calculating prime numbers)
2. Run the function sequentially for a set of inputs
3. Run the function using multiple threads
4. Run the function using multiprocessing
5. Compare and analyze the execution times of each approach

Requirements:
- Use the threading module for the multithreaded approach
- Use the multiprocessing module for the multiprocessing approach
- Measure and report the execution time for each approach
- Provide a clear explanation of the results and how they relate to the GIL

Bonus:
- Experiment with different types of CPU-bound tasks and compare their behavior
- Investigate and implement ways to mitigate the impact of the GIL on multithreaded programs
"""

# Your code here
