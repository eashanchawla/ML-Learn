                                                                                                                                                                                        
"""                                                                                                                                                                                    
 Write a Python script that uses the subprocess module to execute an external command.                                                                                                  
 The command should be 'echo Hello, World!' and capture its output.                                                                                                                     
                                                                                                                                                                                        
 - Use subprocess.run() to execute the command.                                                                                                                                         
 - Print the captured output.                                                                                                                                                           
"""                                                                                                                                                                                    
                                                                                                                                                                                        
import subprocess

# Run the command and capture the output
result = subprocess.run(['echo', 'Hello, World!'], capture_output=True, text=True)

# Print the captured output
print(result.stdout.strip())
                                                                                                                                                                                        
