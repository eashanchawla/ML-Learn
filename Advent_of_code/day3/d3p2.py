import re
from pathlib import Path

file_path = Path(__file__).parent / 'd3.txt'
with open(file_path, 'r') as f:
    data = f.readlines()
digits_found = dict()

def find_number(current_row, index):
    '''Look in both directions to find the number'''
    # what if no extra digits are found? i.e. only this one digit exists? 
    start_index, end_index = index, index
    while start_index>=0 and current_row[start_index-1].isdigit():
        start_index-=1
    while end_index<len(current_row) and current_row[end_index].isdigit():
        end_index+=1
    return int(current_row[start_index:end_index]), start_index, end_index


def check_diagonal(data, i, j):
    '''Look for any digits in it's diagonal vicinity'''
    checks = [[-1, -1], [-1, 0], [1, -1], [0, -1], [0, 1], [-1, 1], [0, 1], [1, 1]]
    for current_check in checks:
        if i+current_check[0]<0 or i+current_check[0]>=len(data) or j+current_check[1]<0 or j+current_check[1]>=len(data[i]):
            # print(f'Skipping {i+current_check[0]}, {j+current_check[1]}')
            # if we find a special character on the first or last 
            # row/record of the text file, we should ignore that as
            # that check will be out of bounds
            continue
        if data[i+current_check[0]][j+current_check[1]].isdigit():
            # print(f'Digit found {data[i+current_check[0]][j+current_check[1]]} at {i+current_check[0]}, {j+current_check[1]}')
            digit_found, start_index, end_index  = find_number(data[i+current_check[0]], j+current_check[1])
            # print(f'Final digit found {digit_found}: {start_index}:{end_index}')\
            if digit_found not in digits_found.keys():
                digits_found[digit_found]=set()
            digits_found[digit_found].add((i, start_index, end_index))
            # print(digits_found[digit_found])


pattern = r'[^\w\s.]'
# convert this to a list of lists
data = [line.strip() for line in data]

for i in range(len(data)):
    character_indices = []
    matches = re.finditer(pattern, data[i])
    for match in matches:
        start_index = match.start()
        check_diagonal(data, i, start_index)

final_sum = 0
for x in digits_found:
    final_sum += (len(digits_found[x]) * x)

print(final_sum)
