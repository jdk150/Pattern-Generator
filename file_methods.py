import numpy as np
import stl_tools

class File_Method:
    def __init__(self, mesh, just_print = False):
        if not just_print:
            self.name = input('What would you like to name the file? (without the file extention) ')
        self.mesh = mesh

class stl_File(File_Method):
    def __init__(self, mesh):
        super().__init__(mesh)
        stl_tools.numpy2stl(self.mesh, self.name + '.stl', scale=1, mask_val = 0.5, force_python=True, square_corners=True)

class Print_Mesh(File_Method):
    def __init__(self, mesh):
        super().__init__(self, mesh, just_print = True)
        for i in range(0, len(self.mesh)):
            row = ''
            for j in range(0, len(self.mesh[i])):
                row += str(int(self.mesh[i][j])) + ' '
            print(row)

class txt_File(File_Method):
    def __init__(self, mesh):
        seper().__init__(self, mesh)
        txtfile = open(self.name + '.txt', 'x')
        for i in range(0, len(self.mesh)):
            row = ''
            for j in range(0, len(self.mesh[i])):
                row += str(int(self.mesh[i][j])) + ' '
            txtfile.write(row + '\n')
        txtfile.close()
    
class stp_File(File_Method):
    def __init__(self, mesh):
        super().__init(self, mesh)
        stpfile = open(self.name + '.stp', 'x')
        stpfile.write('ISO-10303-21;' + '\n')
        stpfile.write('HEADER;' + '\n')
        import time
        t = time.localtime()
        stpfile.write("FILE_NAME('" + self.name + "','" + str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + "T" + str(t[3]) + ":" + str(t[4]) + ":" + str(t[5]) + "');" + "\n")
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
        stpfile.write("#10 = CARTESIAN_POINT('',(0.,0.,1.));" + "\n")
        stpfile.write("#11 = DIRECTION('',(0.,0.,1.));" + "\n")
        stpfile.write("#12 = DIRECTION('',(1.,0.,0.));" + "\n")
        stpfile.write("#13 = SHELL_BASED_SURFACE_MODEL('',(#14));" + "\n")
        open_shell = "#14 = OPEN_SHELL('',("
        plane = "#15 = PLANE('',#9);" + "\n"
        faces = []
        points_ind = []
        points_number = []
        n = 16
        len14 = 17
        i = 0
        while i < len(self.mesh):
            width = 1
            while i + width < len(self.mesh) and all(self.mesh[i] == self.mesh[i + width]):
                width += 1
            j = 0
            while j < len(self.mesh[i]):
                height = 1
                while j + height < len(self.mesh[i]) and self.mesh[i][j] == self.mesh[i][j + height]:
                    height += 1
                if self.mesh[i][j] == 1:
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
                    NW = 0
                    NE = 0
                    if points_ind.count((i,j)) > 0:
                        NW = points_number[points_ind.index((i,j))]
                        if points_ind.count((i + width,j)) > 0:
                            NE = points_number[points_ind.index((i + width,j))]
                        else:
                            NE = n + 27
                    else:
                        NW = n + 27
                        if points_ind.count((i + width,j)) > 0:
                            NE = points_number[points_ind.index((i + width,j))]
                        else:
                            NE = n + 29
                    
                    faces.append([])
                    faces[-1].append("#" + str(n) + " = ADVANCED_FACE('',(#" + str(n+1) + "),#15,.T.);" + "\n")
                    faces[-1].append("#" + str(n + 1) + " = FACE_BOUND('',#" + str(n+2) + ",.T.);" + "\n")
                    faces[-1].append("#" + str(n + 2) + " = EDGE_LOOP('',(#" + str(n+3) + ",#" + str(n+5) + ",#" + str(n+7) + ",#" + str(n+9) + "));" + "\n")
                    
                    faces[-1].append("#" + str(n + 3) + " = ORIENTED_EDGE('',*,*,#" + str(n+4) + ",.T.);" + "\n")
                    faces[-1].append("#" + str(n + 4) + " = EDGE_CURVE('',#" + str(NW) + ",#" + str(NE) + ",#" + str(n+11) + ",.T.);" + "\n")
                    faces[-1].append("#" + str(n + 5) + " = ORIENTED_EDGE('',*,*,#" + str(n+6) + ",.T.);" + "\n")
                    faces[-1].append("#" + str(n + 6) + " = EDGE_CURVE('',#" + str(NE) + ",#" + str(n+23) + ",#" + str(n+14) + ",.T.);" + "\n")
                    faces[-1].append("#" + str(n + 7) + " = ORIENTED_EDGE('',*,*,#" + str(n+8) + ",.T.);" + "\n")
                    faces[-1].append("#" + str(n + 8) + " = EDGE_CURVE('',#" + str(n+23) + ",#" + str(n+25) + ",#" + str(n+17) + ",.T.);" + "\n")
                    faces[-1].append("#" + str(n + 9) + " = ORIENTED_EDGE('',*,*,#" + str(n+10) + ",.T.);" + "\n")
                    faces[-1].append("#" + str(n + 10) + " = EDGE_CURVE('',#" + str(n+25) + ",#" + str(NW) + ",#" + str(n+20) + ",.T.);" + "\n")
                    
                    faces[-1].append("#" + str(n + 11) + " = LINE('',#" + str(NW+1) + ",#" + str(n+12) + ");" + "\n")
                    faces[-1].append("#" + str(n + 12) + " = VECTOR('',#" + str(n+13) + "," + str(width) + ".);" + "\n")
                    faces[-1].append("#" + str(n + 13) + " = DIRECTION('',(1.,0.,0.));" + "\n")
                    faces[-1].append("#" + str(n + 14) + " = LINE('',#" + str(NE+1) + ",#" + str(n+15) + ");" + "\n")
                    faces[-1].append("#" + str(n + 15) + " = VECTOR('',#" + str(n+16) + "," + str(height) + ".);" + "\n")
                    faces[-1].append("#" + str(n + 16) + " = DIRECTION('',(0.,1.,0.));" + "\n")
                    faces[-1].append("#" + str(n + 17) + " = LINE('',#" + str(n+24) + ",#" + str(n+18) + ");" + "\n")
                    faces[-1].append("#" + str(n + 18) + " = VECTOR('',#" + str(n+19) + "," + str(width) + ".);" + "\n")
                    faces[-1].append("#" + str(n + 19) + " = DIRECTION('',(-1.,0.,0.));" + "\n")
                    faces[-1].append("#" + str(n + 20) + " = LINE('',#" + str(n+26) + ",#" + str(n+21) + ");" + "\n")
                    faces[-1].append("#" + str(n + 21) + " = VECTOR('',#" + str(n+22) + "," + str(height) + ".);" + "\n")
                    faces[-1].append("#" + str(n + 22) + " = DIRECTION('',(0.,-1.,0.));" + "\n")
                    
                    faces[-1].append("#" + str(n + 23) + " = VERTEX_POINT('',#" + str(n+24) + ");" + "\n")
                    faces[-1].append("#" + str(n + 24) + " = CARTESIAN_POINT('',(" + str(i+width) + ".," + str(j+height) + ".,1.));" + "\n")
                    points_ind.append((i + width, j + height))
                    points_number.append(n + 23)
                    faces[-1].append("#" + str(n + 25) + " = VERTEX_POINT('',#" + str(n+26) + ");" + "\n")
                    faces[-1].append("#" + str(n + 26) + " = CARTESIAN_POINT('',(" + str(i) + ".," + str(j+height) + ".,1.));" + "\n")
                    points_ind.append((i, j + height))
                    points_number.append(n + 25)
                    if NW > n:
                        faces[-1].append("#" + str(NW) + " = VERTEX_POINT('',#" + str(NW+1) + ");" + "\n")
                        faces[-1].append("#" + str(NW+1) + " = CARTESIAN_POINT('',(" + str(i) + ".," + str(j) + ".,1.));" + "\n")
                        points_ind.append((i, j))
                        points_number.append(NW)
                        n += 2
                    if NE > n:
                        faces[-1].append("#" + str(NE) + " = VERTEX_POINT('',#" + str(NE+1) + ");" + "\n")
                        faces[-1].append("#" + str(NE+1) + " = CARTESIAN_POINT('',(" + str(i+width) + ".," + str(j) + ".,1.));" + "\n")
                        points_ind.append((i + width, j))
                        points_number.append(NE)
                        n += 2
                    n += 27
                j += height
            i += width
        open_shell += "));" + "\n"
        stpfile.write(open_shell)
        stpfile.write(plane)
        for i in range(0, len(faces)):
            for j in range(0, len(faces[i])):
                stpfile.write(faces[i][j])
        stpfile.write("ENDSEC;" + "\n")
        stpfile.write("END-ISO-10303-21;" + "\n")
        stpfile.close()
