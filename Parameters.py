import Pattern
import file_methods
import numpy as np

#creates the mesh as a numpy array stored as Mesh.mesh
pattern_dict = {'columnar':Pattern.Columnar, 'ashlar':Pattern.Ashlar, 'pseudo random':Pattern.PseudoRandom, 'pseudorandom':Pattern.PseudoRandom, 'pseudo_random':Pattern.PseudoRandom, 'pr':Pattern.PseudoRandom}
pattern = input('What pattern would you like? ').lower()
Mesh = pattern_dict[pattern]()

#turns the array into the desired file
file_dict = {'stl':file_methods.stl_File, 'just print':file_methods.Print_Mesh, 'print':file_methods.Print_Mesh, 'txt':file_methods.txt_File, 'stp':file_methods.stp_File, 'step':file_methods.stp_File, 'p21':file_methods.stp_File}
file_type = input('What kind of file would you like? ').lower()
file_dict[file_type](Mesh.mesh)
