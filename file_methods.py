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
    
    def stp_file(mesh):
    name = input('What should the file be called? (sans ".stp") ')
    stpfile = open(name + '.stp', 'x')
    stpfile.write('ISO-10303-21;' + '\n')
    stpfile.write('HEADER;' + '\n')
    import time
    t = time.localtime()
    stpfile.write("FILE_NAME('" + name + "','" + str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + "T" + str(t[3]) + ":" + str(t[4]) + ":" + str(t[5]) + "');" + "\n")
    stpfile.write("FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));" + "\n")
    stpfile.write('ENDSEC;' + '\n')
    stpfile.write('DATA;' + '\n')
    stpfile.write("#1 = SHAPE_DEFINITION_REPRESENTATION(#2,#8);" + "\n")
    stpfile.write("#2 = PRODUCT_DEFINITION_SHAPE('','',#3);" + "\n")
    stpfile.write("#3 = PRODUCT_DEFINITION('','',#4,#7);" + "\n")
    stpfile.write("#4 = PRODUCT_DEFINITION_FORMATION('','',#5);" + "\n")
    stpfile.write("#5 = PRODUCT('','','',(#6));" + "\n")
    stpfile.write("#6 = PRODUCT_CONTEXT('','','');" + "\n")
    stpfile.write("#7 = PRODUCT_DEFINITION_CONTEXT('','','');" + "\n")
    stpfile.write("#8 = MANIFOLD_SURFACE_SHAPE_REPRESENTATION('',(#9,#13),'');" + "\n")
    stpfile.write("#9 = AXIS2_PLACEMENT_3D('',#10,#11,#12);" + "\n")
    stpfile.write("#10 = CARTESIAN_POINT('',(0.,0.,0.));" + "\n")
    stpfile.write("#11 = DIRECTION('',(0.,0.,1.));" + "\n")
    stpfile.write("#12 = DIRECTION('',(1.,0.,0.));" + "\n")
    stpfile.write("#13 = SHELL_BASED_SURFACE_MODEL('',(#14));" + "\n")
    open_shell = "#14 = OPEN_SHELL('',("
    faces = []
    n = 15
    len14 = 17
    for i in range(0, len(mesh)):
        for j in range(0, len(mesh[i])):
            if mesh[i][j] == 1:
                if len(faces) == 0:
                    open_shell += "#" + str(n)
                    len14 = len(open_shell) - 4
                else:
                    new_num = ",#" + str(n)
                    if len14 + len(new_num) > 70:
                        open_shell += ",\n    " + new_num[1:]
                        len14 = len(new_num) - 1
                    else:
                        open_shell += new_num
                        len14 += len(new_num)
                faces.append([])
                faces[-1].append("#" + str(n) + " = ADVANCED_FACE('',(#" + str(n+1) + "),#" + str(n+31) + ",.T.);" + "\n")
                faces[-1].append("#" + str(n + 1) + " = FACE_BOUND('',#" + str(n+2) + ",.T.);" + "\n")
                faces[-1].append("#" + str(n + 2) + " = EDGE_LOOP('',(#" + str(n+11) + ",#" + str(n+16) + ",#" + str(n+21) + ",#" + str(n+26) + "));" + "\n")
                faces[-1].append("#" + str(n + 3) + " = VERTEX_POINT('',#" + str(n+4) + ");" + "\n")
                faces[-1].append("#" + str(n + 4) + " = CARTESIAN_POINT('',(" + str(i) + ".," + str(j) + ".,1.));" + "\n")
                faces[-1].append("#" + str(n + 5) + " = VERTEX_POINT('',#" + str(n+6) + ");" + "\n")
                faces[-1].append("#" + str(n + 6) + " = CARTESIAN_POINT('',(" + str(i+1) + ".," + str(j) + ".,1.));" + "\n")
                faces[-1].append("#" + str(n + 7) + " = VERTEX_POINT('',#" + str(n+8) + ");" + "\n")
                faces[-1].append("#" + str(n + 8) + " = CARTESIAN_POINT('',(" + str(i+1) + ".," + str(j+1) + ".,1.));" + "\n")
                faces[-1].append("#" + str(n + 9) + " = VERTEX_POINT('',#" + str(n+10) + ");" + "\n")
                faces[-1].append("#" + str(n + 10) + " = CARTESIAN_POINT('',(" + str(i) + ".," + str(j+1) + ".,1.));" + "\n")
                faces[-1].append("#" + str(n + 11) + " = ORIENTED_EDGE('',*,*,#" + str(n+12) + ",.T.);" + "\n")
                faces[-1].append("#" + str(n + 12) + " = EDGE_CURVE('',#" + str(n+3) + ",#" + str(n+5) + ",#" + str(n+13) + ",.T.);" + "\n")
                faces[-1].append("#" + str(n + 13) + " = LINE('',#" + str(n+4) + ",#" + str(n+14) + ");" + "\n")
                faces[-1].append("#" + str(n + 14) + " = VECTOR('',#" + str(n+15) + ",1.);" + "\n")
                faces[-1].append("#" + str(n + 15) + " = DIRECTION('',(" + str(1) + ".," + str(0) + ".,0.));" + "\n")
                faces[-1].append("#" + str(n + 16) + " = ORIENTED_EDGE('',*,*,#" + str(n+17) + ",.T.);" + "\n")
                faces[-1].append("#" + str(n + 17) + " = EDGE_CURVE('',#" + str(n+5) + ",#" + str(n+7) + ",#" + str(n+18) + ",.T.);" + "\n")
                faces[-1].append("#" + str(n + 18) + " = LINE('',#" + str(n+6) + ",#" + str(n+19) + ");" + "\n")
                faces[-1].append("#" + str(n + 19) + " = VECTOR('',#" + str(n+20) + ",1.);" + "\n")
                faces[-1].append("#" + str(n + 20) + " = DIRECTION('',(" + str(0) + ".," + str(1) + ".,0.));" + "\n")
                faces[-1].append("#" + str(n + 21) + " = ORIENTED_EDGE('',*,*,#" + str(n+22) + ",.T.);" + "\n")
                faces[-1].append("#" + str(n + 22) + " = EDGE_CURVE('',#" + str(n+7) + ",#" + str(n+9) + ",#" + str(n+23) + ",.T.);" + "\n")
                faces[-1].append("#" + str(n + 23) + " = LINE('',#" + str(n+8) + ",#" + str(n+24) + ");" + "\n")
                faces[-1].append("#" + str(n + 24) + " = VECTOR('',#" + str(n+25) + ",1.);" + "\n")
                faces[-1].append("#" + str(n + 25) + " = DIRECTION('',(" + str(-1) + ".," + str(0) + ".,0.));" + "\n")
                faces[-1].append("#" + str(n + 26) + " = ORIENTED_EDGE('',*,*,#" + str(n+27) + ",.T.);" + "\n")
                faces[-1].append("#" + str(n + 27) + " = EDGE_CURVE('',#" + str(n+9) + ",#" + str(n+3) + ",#" + str(n+28) + ",.T.);" + "\n")
                faces[-1].append("#" + str(n + 28) + " = LINE('',#" + str(n+10) + ",#" + str(n+29) + ");" + "\n")
                faces[-1].append("#" + str(n + 29) + " = VECTOR('',#" + str(n+30) + ",1.);" + "\n")
                faces[-1].append("#" + str(n + 30) + " = DIRECTION('',(" + str(0) + ".," + str(-1) + ".,0.));" + "\n")
                faces[-1].append("#" + str(n + 31) + " = PLANE('',#" + str(n+32) + ");" + "\n")
                faces[-1].append("#" + str(n + 32) + " = AXIS2_PLACEMENT_3D('',#" + str(n+33) + ",#" + str(n+34) + ",#" + str(n+35) + ");" + "\n")
                faces[-1].append("#" + str(n + 33) + " = CARTESIAN_POINT('',(0.,0.,1.));" + "\n")
                faces[-1].append("#" + str(n + 34) + " = DIRECTION('',(0.,0.,1.));" + "\n")
                faces[-1].append("#" + str(n + 35) + " = DIRECTION('',(1.,0.,0.));" + "\n")
                n += 36
    open_shell += "));" + "\n"
    stpfile.write(open_shell)
    for i in range(0, len(faces)):
        for j in range(0, len(faces[i])):
            stpfile.write(faces[i][j])
    stpfile.write("ENDSEC;" + "\n")
    stpfile.write("END-ISO-10303-21;" + "\n")
    stpfile.close()