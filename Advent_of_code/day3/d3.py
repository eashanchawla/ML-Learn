'''Not the most efficient code
I am writing this at 2 am, as I try to stay awake to watch the Australian Open Men's Singles Finals between
Jannik Sinner and Daniil Medvedev. My money's on Daniil. But I am so sleepy that I can myself writing bad code
'''

import re
from pathlib import Path

gear_ratio=0
file_path = Path(__file__).parent / 'd3.txt'
with open(file_path, 'r') as f:
    data = f.readlines()
digits_found = dict()

def find_number(current_row, index):
    '''Look in both directions to find the number'''
    # what if no extra digits are found? i.e. only this one digit exists? 
    start_index, end_index = index, index
    while start_index>0 and current_row[start_index-1].isdigit():
        start_index-=1
    while end_index<len(current_row) and current_row[end_index].isdigit():
        end_index+=1

    # print(f'{int(current_row[start_index:end_index])}, {start_index}: {end_index}')
    return int(current_row[start_index:end_index]), start_index, end_index

def update_gear_ratio(digits_found):
    global gear_ratio
    gear_contestants=list()
    for digit in digits_found:
        for _ in range(len(digits_found[digit])):
            gear_contestants.append(digit)
    if len(gear_contestants)==2:
        # print(digits_found)
        gear_ratio += (gear_contestants[0]*gear_contestants[1])


def check_diagonal(data, i, j):
    '''Look for any digits in it's diagonal vicinity'''
    digits_found_here = dict()
    found_count=0
    checks = [[-1, -1], [-1, 0], [1, -1], [0, -1], [0, 1], [-1, 1], [0, 1], [1, 1], [1,0]]
    for current_check in checks:
        if i+current_check[0]<0 or i+current_check[0]>=len(data) or j+current_check[1]<0 or j+current_check[1]>=len(data[i]):
            # if we find a special character on the first or last 
            # row/record of the text file, we should ignore that as
            # that check will be out of bounds
            continue
        if data[i+current_check[0]][j+current_check[1]].isdigit():
            digit_found, start_index, end_index  = find_number(data[i+current_check[0]], j+current_check[1])
            if digit_found not in digits_found_here.keys():
                digits_found_here[digit_found]=set()
            # digits_found_here.append(digit_found)
            digits_found_here[digit_found].add((i+current_check[0], start_index, end_index))
    print(digits_found_here)
    update_gear_ratio(digits_found_here)
        

pattern = r'[*]'
# convert this to a list of lists
data = [line.strip() for line in data]

for i in range(len(data)):
    character_indices = []
    matches = re.finditer(pattern, data[i])
    for match in matches:
        start_index = match.start()
        check_diagonal(data, i, start_index)

print(gear_ratio)