# Ashton Cole
# COE 332: Homework 1

# EXERCISE 3

import names

def name_len(name):
    return len(name.replace(' ', '').replace('\n', ''))

for _ in range(5):
    name = names.get_full_name()
    length = name_len(name)
    print(f'{name} - {length} letters')
