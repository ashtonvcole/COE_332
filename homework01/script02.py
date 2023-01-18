# Ashton Cole
# COE 332: Homework 1

# EXERCISE 2

import names

count = 0
max = 5
while True:
    if count >= max:
        break
    name = names.get_full_name()
    if len(name) == 9:
        print(name)
        count = count + 1
