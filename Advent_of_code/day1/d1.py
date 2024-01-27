import re
with open('./d1p1.txt') as f:
    data = f.readlines()

data = [val.strip() for val in data]
data = [val.replace(
    'one', 'one1one').replace('two', 'two2two').replace('three', 'three3three').replace(
        'four', 'four4four').replace('five', 'five5five').replace('six', 'six6six').replace(
            'seven', 'seven7seven').replace('eight', 'eight8eight').replace('nine', 'nine9nine')
            for val in data]

numbers_found = [re.findall('\d' ,x) for x in data]
print(sum([int(numbers[0] + numbers[-1]) for numbers in numbers_found]))


