import sys
import time

def greeting(name):
    print(f"Hey {name}")

if __name__ == '__main__':
    greeting(sys.argv[1])

# Add a timer object to track the time taken for each iteration of the loop
timer = time.time()

for i in range(len(dataset)):
    sample = dataset[i]["audio"]
    result = pipe(sample)
    print(result["text"])
    
    # Calculate the time taken for this iteration and add it to the timer object
    time_taken = time.time() - timer
    timer += time_taken
