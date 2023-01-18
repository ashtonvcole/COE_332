my_shapes = ['circle', 'heart', 'triangle', 'square']

with open('myshapes', 'w') as f:
    for shape in my_shapes:
        f.write(f'{shape}\n')
