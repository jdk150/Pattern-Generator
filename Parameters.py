import Pattern
import file_methods
import numpy as np

#creates the mesh as a numpy array stored as Mesh.mesh
pattern_dict = {'columnar':Columnar, 'ashlar':Ashlar, 'pseudo random':PseudoRandom, 'pseudorandom':PseudoRandom, 'pseudo_random':PseudoRandom, 'pr':PseudoRandom}
pattern = input('What pattern would you like? ').lower()
Mesh = pattern_dict[pattern]()

#turns the array into the desired file
file_dict = {'stl':stl_file, 'just print':print_mesh, 'txt':txt_file}
file_type = input('What kind of file would you like? ').lower()
file_dict[file_type](Mesh.mesh)
