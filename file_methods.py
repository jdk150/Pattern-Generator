import numpy as np
import stl_tools

def stl_file(mesh):
    name = input('What should the file be called? (sans ".stl") ')
    stl_tools.numpy2stl(mesh, name + '.stl', scale=1, mask_val = 0.5, force_python=True, square_corners=True)

def print_mesh(mesh):
    for i in range(0, len(mesh)):
        row = ''
        for j in range(0, len(mesh[i])):
            row += str(int(mesh[i][j])) + ' '
        print(row)

def txt_file(mesh):
    name = input('What should the file be called? (sans ".txt") ')
    txtfile = open(name + '.txt', 'x')
    for i in range(0, len(mesh)):
        row = ''
        for j in range(0, len(mesh[i])):
            row += str(int(mesh[i][j])) + ' '
        txtfile.write(row + '\n')
    txtfile.close()