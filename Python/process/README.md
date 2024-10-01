# Subprocess ye hua load

## Understanding the Difference Between Multi-threading, Multi-processing, and Async

1. **Multi-threading**
   - Multiple threads in a single [process](#what-is-a-single-process).

## What is a Single Process?

An instance of a program executed by the OS.

### What's Involved in Running a Process?

Let's use the analogy of a chef cooking butter chicken in a kitchen.

The chef needs their:
1. **Recipe (the code)**: A list of instructions for the chef to follow.
2. **Chef's Notebook (Process Control Block)**: Keeps track of everything about this dish.
   - Name of the dish (process ID)
   - Which step it is on (program counter)
   - Utensils being used (CPU registers)
   - When it's their turn to use the stove (CPU scheduling)
   - Where ingredients are stored (memory management)

3. **The Kitchen (Memory)**:
   - **Pantry (Data section)**: Stores ingredients.
   - **Counter space (Heap)**: Extra space for preparation.
   - **Cutting board (Stack)**: Manages function calls.

### How a Process Runs

#### Starting the Recipe (Process Creation)

The kitchen manager (OS) sets up a new workspace for the chef.
It allocates RAM for the process, loading the recipe (program code) and setting up initial data.
A new chef's notebook (PCB) is created with initial information.

#### Chef Begins Work (Process Execution)

The chef (CPU) starts reading and following the recipe instructions.
They use ingredients from the pantry (data section) as needed.
When they need extra space, they use the counter (heap) for preparation.
For each step or sub-recipe (function call), they use a new tray on the cutting board (stack).

#### Using Kitchen Resources

The chef uses appliances (I/O operations) as instructed by the recipe.
They might communicate with other chefs (inter-process communication) if needed.

#### Kitchen Manager Oversight

The manager regularly checks on all chefs, deciding who gets to use the kitchen (CPU scheduling).
If a chef needs to wait (e.g., for an appliance to finish), the manager might let another chef work.

#### Pausing and Resuming Work

When it's time to switch chefs, the current chef quickly notes their exact status in their notebook (PCB).
This includes which instruction they were on, what's on their cutting board, what they were preparing on the counter, etc.
When it's their turn again, they consult their notebook to know exactly where to resume.

#### Memory Management

If the chef needs more counter space (heap memory), they ask the manager for more.
If they're done with some counter space, they let the manager know it can be reused.
The stack (cutting board) automatically grows and shrinks with each function call and return.

#### Finishing Up

When the recipe is complete, the chef informs the manager.
The manager cleans up the workspace, freeing all allocated memory and resources.

Throughout this process:
- The actual work (data processing) happens in RAM, represented by our kitchen space.
- The chef's notebook (PCB) doesn't store the actual data but keeps track of where everything is and what's happening.
- The chef (CPU) actively works with the data in RAM, reading instructions and manipulating information as directed by the recipe (program code).

### In Python

- **Single process**: Refers to a single instance of the Python interpreter.

## Subprocess

- This module allows us to execute and manage additional processes, like running Python scripts or other applications (like ffmpeg).

## Learning Path

1. **[basic_subprocess.py](basic_subprocess.py)**: Introduction to subprocess.run() for executing simple commands.
2. **[handle_output_error.py](handle_output_error.py)**: Capturing both stdout and stderr from a subprocess.
3. **[subprocess_stdout.py](subprocess_stdout.py)**: Focusing on capturing and handling stdout.
4. **[subprocess_stderr.py](subprocess_stderr.py)**: Focusing on capturing and handling stderr.
5. **[subprocess_pipe.py](subprocess_pipe.py)**: Using subprocess to create pipes between commands.
6. **[subprocess_ffmpeg_mic.py](subprocess_ffmpeg_mic.py)**: Advanced usage with ffmpeg to capture audio and use threading.Queue.

Each file builds on the concepts of the previous ones, gradually introducing more complex subprocess operations.

### Subprocess module

When you run a subprocess using subprocess.run() or subprocess.Popen(), it creates an instance of the shell that knows what program ls refers to. This allows you to use the same command in your Python script and have it executed as if it were running directly on your system.

#### Shell Environment

The subprocess inherits the existing shell environment, which includes:

- Current working directory
- Command history
- Other settings

This means that the subprocess can interact with the output of other commands without needing to create a new interpreter instance.

#### Creating New Interpreter Instances

When you use Popen(), it creates a new process that runs the specified command and captures its output. This is equivalent to running another Python script.

Here's an example:

```python
import subprocess

# Create two subprocesses: one running ls -l and another running python script
subprocess.run(["ls", "-l"], stdout=subprocess.PIPE)
subprocess.Popen(["python", "script.py"])
```

In this case, both subprocesses will run independently of each other. The ls command in the first subprocess will execute as if it were running directly on your system, while the Python script in the second subprocess will be executed by a separate process.

#### Key Takeaways

- Subprocesses create an instance of the shell that knows what program ls refers to.
- The subprocess inherits the existing shell environment.
- Creating new interpreter instances using Popen() is equivalent to running another Python script.


#### PIPE
- Lets us read a buffered stream of bytes
- subprocess.PIPE is a file like object, that lets us read the stdout or stdedrr with .readline() or .read() type methods

# Subprocess and Byte Streams in Python

## Overview of `subprocess.popen` and Byte Streams
- The `subprocess.popen` function allows asynchronous execution of external commands, providing more control over subprocesses.
- You can interact with a process’s `stdin`, `stdout`, and `stderr` using pipes (`subprocess.PIPE`), which are **byte streams**.

## Key Differences Between `subprocess.popen` and `subprocess.run`
- **`subprocess.popen`**: Allows real-time interaction with a running process. You can check its status, read/write data during its execution, and control its lifecycle.
- **`subprocess.run`**: Synchronous execution that waits for the command to complete and returns the output or errors after the process finishes.

## Working with Byte Streams
- Byte streams represent raw binary data (not strings).
- Data in `stdout` and `stderr` of a subprocess is returned as **bytes**, not strings.
- To work with textual data, you need to **decode** the bytes using a character encoding (e.g., UTF-8).

## Example: Capturing Output from a Subprocess
```python
import subprocess

# Start the process and capture stdout in a pipe (byte stream)
process = subprocess.Popen(['echo', 'Hello, World!'], stdout=subprocess.PIPE)

# Read one line from stdout (as bytes)
output = process.stdout.readline()

# Decode the byte stream to a string
decoded_output = output.decode('utf-8')
print(decoded_output)  # Output: 'Hello, World!\n'
```