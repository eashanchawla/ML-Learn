# Subprocess

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

- This module allows us to execute, manage additional processes, like running Python scripts or other applications (like ffmpeg).
