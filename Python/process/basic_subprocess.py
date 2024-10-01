                                                                                                                                                                                        
"""                                                                                                                                                                                    
 Write a Python script that uses the subprocess module to execute an external command.                                                                                                  
 The command should be 'echo Hello, World!' and capture its output.                                                                                                                     
                                                                                                                                                                                        
 - Use subprocess.run() to execute the command.                                                                                                                                         
 - Print the captured output.                                                                                                                                                           
"""                                                                                                                                                                                    

import subprocess

output = subprocess.run(["echo", "Hello, World!"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print(output.stdout.decode())