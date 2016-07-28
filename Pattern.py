import numpy as np
import math

class Pattern:
    def __init__(self, pr = False):
        
        if pr:
            print('When making a pseudo random mesh do not use exact nanometer measurements.')
            print('Pseudo random meshes are not scaled down by the greates common divisor of all of the parameters.')
            print('Doing so would effectively make the mesh less random.')
        #ask for the independant parameters
        height = int(input('What is the height of the mesh in nm? '))
        width = int(input('What is the width of the mesh in nm? '))
        frame = int(input('How thick do you want the border for your mesh in nm? '))
        slit_height = int(input('What is the slit height in nm? '))
        pitch = int(input('What is the pitch in nm? '))
        strut_width = int(input('What is the strut width in nm? '))
        fill = input('Do you want to fill in all the one width slits on the edges? ').lower()
        #these are arbitrary values, any statements don't like it if you compare strings to ints
        if fill[0] == 'y':
            fill = 2
        else:
            fill = 0
        #'-frame' is is usded instead of -'frame' for array indices because 0 == -0
        self.ind_param = {'height':height, 'width':width, 'frame':frame, 'pitch':pitch, 'slit height':slit_height, 'strut width':strut_width, 'strut height': pitch - slit_height, '-frame h':height + frame, '-frame w':width + frame, 'fill':fill}
        self.factor = math.gcd(height, math.gcd(width, math.gcd(frame, math.gcd(slit_height, math.gcd(pitch, strut_width)))))
        self.mesh = np.zeros(0)
        self.dep_param = {}

class Columnar(Pattern):
    def __init__(self):
        super().__init__()
        #ask for the Pattern dependant parameters
        slit_width = int(input('What is the slit width in nm? '))
        self.dep_param = {'slit width':slit_width}
        
        #minimizing the parameters
        self.factor = math.gcd(slit_width, self.factor)
        self.ind_param['height'] //= self.factor
        self.ind_param['width'] //= self.factor
        self.ind_param['frame'] //= self.factor
        self.ind_param['pitch'] //= self.factor
        self.ind_param['slit height'] //= self.factor
        self.ind_param['strut width'] //= self.factor
        self.ind_param['strut height'] //= self.factor
        self.ind_param['-frame h'] //= self.factor
        self.ind_param['-frame w'] //= self.factor
        self.dep_param['slit width'] //= self.factor
        if any(np.array(list(self.ind_param.values()) + list(self.dep_param.values())) == 1):
            self.ind_param['height'] *= 2
            self.ind_param['width'] *= 2
            self.ind_param['frame'] *= 2
            self.ind_param['pitch'] *= 2
            self.ind_param['slit height'] *= 2
            self.ind_param['strut width'] *= 2
            self.ind_param['-frame h'] *= 2
            self.ind_param['-frame w'] *= 2
            self.dep_param['slit width'] *= 2
        
        #create the mesh as a numpy array
        self.mesh = np.zeros((self.ind_param['height'] + 2*self.ind_param['frame'], self.ind_param['width'] + 2*self.ind_param['frame']))
        #fill in the border/frame
        self.mesh[:self.ind_param['frame']] = 1
        self.mesh[self.ind_param['-frame h']:] = 1
        self.mesh[:,:self.ind_param['frame']] = 1
        self.mesh[:,self.ind_param['-frame w']:] = 1
        
        #creating a row
        row = np.zeros((self.ind_param['pitch'], self.ind_param['width']))
        #passes over a slit width and then fill in a strut, sice the mesh is already filled with zeros
        #indices greater than the arrays dimentions are automatically igored
        ind = 0
        while ind < len(row[0]):
            ind += self.dep_param['slit width']
            row[0][ind:ind + self.ind_param['strut width']] = 1
            ind += self.ind_param['strut width']
        #fill in one-width slits
        if self.ind_param['fill'] == 2 and row[0,-2] - row[0,-1] == 1:
            row[0,-1] = 1
        #fills in the rest of the pitch
        row[:self.ind_param['slit height']] = row[0]
        row[self.ind_param['slit height']:] = 1
        
        #filling in the mesh
        ind = self.ind_param['frame']
        while ind < len(self.mesh) - self.ind_param['frame']:
            if ind + len(row) <= len(self.mesh) - self.ind_param['frame']:
                self.mesh[ind:ind + len(row), self.ind_param['frame']:self.ind_param['-frame w']] = row
            else:
                self.mesh[ind:self.ind_param['-frame h'], self.ind_param['frame']:self.ind_param['-frame w']] = row[:len(self.mesh) - self.ind_param['frame'] - ind]
            ind += len(row)

class Ashlar(Pattern):
    def __init__(self):
        super().__init__()
        #ask for the Pattern dependant parameters
        slit_width = int(input('What is the slit width in nm? '))
        self.dep_param = {'slit width': slit_width, 'even/odd slit+strut':self.ind_param['strut width'] + slit_width}
        
        #minimizing the parameters
        self.factor = math.gcd(slit_width, self.factor)
        self.ind_param['height'] //= self.factor
        self.ind_param['width'] //= self.factor
        self.ind_param['frame'] //= self.factor
        self.ind_param['pitch'] //= self.factor
        self.ind_param['slit height'] //= self.factor
        self.ind_param['strut width'] //= self.factor
        self.ind_param['strut height'] //= self.factor
        self.ind_param['-frame h'] //= self.factor
        self.ind_param['-frame w'] //= self.factor
        self.dep_param['slit width'] //= self.factor
        self.dep_param['even/odd slit+strut'] //= self.factor
        self.dep_param['even/odd slit+strut'] = self.dep_param['even/odd slit+strut']%2
        if any(np.array(list(self.ind_param.values()) + list(self.dep_param.values())) == 1):
            self.ind_param['height'] *= 2
            self.ind_param['width'] *= 2
            self.ind_param['frame'] *= 2
            self.ind_param['pitch'] *= 2
            self.ind_param['slit height'] *= 2
            self.ind_param['strut width'] *= 2
            self.ind_param['-frame h'] *= 2
            self.ind_param['-frame w'] *= 2
            self.dep_param['slit width'] *= 2
        
        #create the mesh as a numpy array
        self.mesh = np.zeros((self.ind_param['height'] + 2*self.ind_param['frame'], self.ind_param['width'] + 2*self.ind_param['frame']))
        #fill in the border/frame
        self.mesh[:self.ind_param['frame']] = 1
        self.mesh[self.ind_param['-frame h']:] = 1
        self.mesh[:,:self.ind_param['frame']] = 1
        self.mesh[:,self.ind_param['-frame w']:] = 1
        
        #creating the first row
        row = np.zeros((self.ind_param['pitch']*2, self.ind_param['width']))
        #passes over a slit width and then fill in a strut, sice the mesh is already filled with zeros
        #indices greater than the arrays dimentions are automatically ignored
        ind = 0
        while ind < len(row[0]):
            ind += self.dep_param['slit width']
            row[0][ind:ind + self.ind_param['strut width']] = 1
            ind += self.ind_param['strut width']
        #fill in one-width slits
        if self.ind_param['fill'] == 2 and row[0,-2] - row[0,-1] == 1:
            row[0,-1] = 1
        #fill in the rest of the pitch
        row[:self.ind_param['slit height']] = row[0]
        row[self.ind_param['slit height']:self.ind_param['pitch']] = 1
        
        #creating the second row 
        #since the second row is offset 50%, this part fill in the first half of a slit before filling in the rest of the row normally
        strut_start = (self.dep_param['slit width'] - self.ind_param['strut width'])//2
        if self.dep_param['slit width'] >= self.ind_param['strut width']:
            row[self.ind_param['pitch']][strut_start:strut_start + self.ind_param['strut width']] = 1
        else:
            row[self.ind_param['pitch']][:strut_start + self.ind_param['strut width']] = 1
        #fill in the rest of the row normally
        ind = strut_start + self.ind_param['strut width']
        while ind < len(row[0]):
            ind += self.dep_param['slit width']
            row[self.ind_param['pitch']][ind:ind + self.ind_param['strut width']] = 1
            ind += self.ind_param['strut width']
        #fill in one-width slits
        if self.ind_param['fill'] == 2:
            if row[self.ind_param['pitch'],-2] - row[self.ind_param['pitch'],-1] == 1:
                row[self.ind_param['pitch'],-1] = 1
            if row[self.ind_param['pitch'],1] - row[self.ind_param['pitch'],0] == 1:
                row[self.ind_param['pitch'],0] = 1
        row[self.ind_param['pitch']:self.ind_param['pitch'] + self.ind_param['slit height']] = row[self.ind_param['pitch']]
        row[self.ind_param['pitch'] + self.ind_param['slit height']:] = 1
        
        #filling in the mesh
        ind = self.ind_param['frame']
        while ind < len(self.mesh) - self.ind_param['frame']:
            if ind + len(row) <= len(self.mesh) - self.ind_param['frame']:
                self.mesh[ind:ind + len(row), self.ind_param['frame']:self.ind_param['-frame w']] = row
            else:
                self.mesh[ind:self.ind_param['-frame h'], self.ind_param['frame']:self.ind_param['-frame w']] = row[:len(self.mesh) - self.ind_param['frame'] - ind]
            ind += len(row)

class PseudoRandom(Pattern):
    def __init__(self):
        super().__init__(pr = True)
        #the pattern dependant parameters and the so far unrandomized parameters
        self.dep_param = {'slit width':lambda:0, 'offset':lambda:0}
        unused_params = ['slit width', 'offset', 'strut placement']
        
        #the random functions if they take up more than one line
        def random_strut_placement(num_struts, min_slit, h):
            #if the current strut spacing list is empty it creates a new list of spaces,
            #otherwise it just deletes the first entry in the list and returns it
            if len(self.dep_param['strut spacing']) == 0:
                #first we create a list of all of the places a strut could possibly start
                #and a place to store all of the randomly selected indeces
                strut_inds = []
                strut_spacing = []
                for i in range(0, h):
                    strut_inds.append(list(np.linspace(0, self.ind_param['width'] - 1, self.ind_param['width'])))
                    strut_spacing.append([])
                num_inds = self.ind_param['width']*h
                #we remove the indices on the ends where there would not be room for a complete strut or a slit of the minimum width
                for i in range(0, h):
                    for j in range(0, min_slit):
                        strut_inds[i].remove(strut_inds[i][0])
                        num_inds -= 1
                for i in range(0, h):
                    for j in range(0, min_slit + self.ind_param['strut width'] - 1):
                        strut_inds[i].remove(strut_inds[i][-1])
                        num_inds -= 1
                #then we randomly pcik values in the lsit untill there are none left or we have reached the desired number of struts
                while num_struts > 0 and num_inds > 0:
                    indw = np.random.randint(0, num_inds)
                    indh=0
                    while indw > len(strut_inds[indh]) - 1:
                        indw -= len(strut_inds[indh])
                        indh += 1
                    strut_spacing[indh].append(int(strut_inds[indh][indw]))
                    #after a value is picked, indices on either side fo it are removed from the list
                    #to pad the new strut with minimum width slits
                    for j in range(strut_spacing[indh][-1] - min_slit - self.ind_param['strut width'] + 1, strut_spacing[indh][-1] + self.ind_param['strut width'] + min_slit):
                        if strut_inds[indh].count(j) > 0:
                            strut_inds[indh].remove(j)
                            num_inds -= 1
                    num_struts -= 1
                for i in range(0, h):
                    strut_spacing[i].sort()
                #if the last strut doesn't happen to line up with the end of the row,
                #a buffer slit is created to make sure the program knows to advance to the next row
                for i in range(0, h):
                    if strut_spacing[i][-1] != self.ind_param['width'] - self.ind_param['strut width']:
                        strut_spacing[i].append(self.ind_param['width']*2)
                #the values in the list are converted from strut indeces to slit widths
                for i in range(0, h):
                    for j in range(1, len(strut_spacing[i])):
                        strut_spacing[i][-j] -= strut_spacing[i][-j - 1] + self.ind_param['strut width']
                #then they are stored in the dependand varialble 'strut spacing'
                for i in range(0, h):
                    for j in range(0, len(strut_spacing[i])):
                        self.dep_param['strut spacing'].append(strut_spacing[i][j])
            #the next value in the list is stored, removed from the list, and then returned
            value = self.dep_param['strut spacing'][0]
            self.dep_param['strut spacing'].remove(value)
            return value
        
        #the random function initializers, they ask for the specific parameters required for each random function
        def default(param):
            minimum = int(input('What is the minimum ' + param + ' in nm? '))
            maximum = int(input('What is the maximum ' + param + ' in nm? '))
            if maximum > minimum:
                self.dep_param[param] = lambda: np.random.random_integers(minimum, maximum)
                unused_params.remove(param)
            else:
                print('the maximum must be greater than the minimum')
                default(param)
            if unused_params.count('strut placement') > 0:
                unused_params.remove('strut placement')
        
        def constant(param):
            value = int(input('What is the ' + param + ' in nm? '))
            self.dep_param[param] = lambda: value
            unused_params.remove(param)
            if unused_params.count('strut placement') > 0:
                unused_params.remove('strut placement')
        
        def random_struts():
            self.dep_param['strut spacing'] = []
            density = input('What do you want the density of struts to be? (#struts/#rows or #struts/mesh) ').lower()
            h=0
            ints = np.array(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
            if len(density) > 4 and density[-4:] == 'mesh':
                if self.ind_param['height']//self.ind_param['pitch'] == self.ind_param['height']/self.ind_param['pitch']:
                    h = self.ind_param['height']//self.ind_param['pitch']
                else:
                    h = self.ind_param['height']//self.ind_param['pitch'] + 1
            else:
                i = 0
                while density[i] != '/':
                    i += 1
                i += 1
                h = ''
                while i < len(density) and any(ints == density[i]):
                    h += density[i]
                    i += 1
                h = int(h)
            num_struts = ''
            i = 0
            while any(ints == density[i]):
                num_struts += density[i]
                i += 1
            num_struts = int(num_struts)
            min_slit = int(input('What is the minimum slit width? '))
            self.dep_param['slit width'] = lambda: random_strut_placement(num_struts, min_slit, h)
            unused_params.clear()
        
        func_init_dict = {'':default, 'default':default, 'uniform distribution':default, 'constant':constant, 'strut placement':random_struts}
        
        #asks what parameters should be randomized and asks what constants the others should be
        param = ''
        while param != 'done' and len(unused_params) > 0:
            param = input('What parameters would you like to randomize? (enter "done" to continue or "help" for a list of parameters) ').lower()
            if param == 'help':
                print(unused_params)
            elif param == 'done':
                while len(unused_params) > 0:
                    func_init_dict['constant'](unused_params[0])
            elif param == 'strut placement':
                func_init_dict[param]()
            elif any(np.array(unused_params) == param):
                func = input('What random function would you like? ').lower()
                func_init_dict[func](param)
            else:
                print('That parameter does not exist or has already been used.')
        
        #create the mesh as a numpy array
        self.mesh = np.zeros((self.ind_param['height'] + 2*self.ind_param['frame'], self.ind_param['width'] + 2*self.ind_param['frame']))
        #fill in the border/frame
        self.mesh[:self.ind_param['frame']] = 1
        self.mesh[self.ind_param['-frame h']:] = 1
        self.mesh[:,:self.ind_param['frame']] = 1
        self.mesh[:,self.ind_param['-frame w']:] = 1
        
        #filling in the mesh
        ind1 = self.ind_param['frame']
        while ind1 < len(self.mesh) - self.ind_param['frame']:
            
            #creating a template for a row
            ind2a = self.ind_param['frame'] + self.dep_param['offset']()
            ind2b = ind2a
            #start at the offset and work backward, filling in struts and then skipping slits
            while ind2b > self.ind_param['frame']:
                self.mesh[ind1][ind2b - self.ind_param['strut width']:ind2b] = 1
                ind2b -= self.ind_param['strut width'] + self.dep_param['slit width']()
            #start at the offset again but this time work forward skipping slits and then filling in struts
            while ind2a < len(self.mesh[0]) - self.ind_param['frame']:
                ind2a += self.dep_param['slit width']()
                self.mesh[ind1][ind2a:ind2a + self.ind_param['strut width']] = 1
                ind2a += self.ind_param['strut width']
            #fill in one-width slits
            if self.ind_param['fill'] == 2:
                if self.mesh[ind1,self.ind_param['-frame w'] - 2] - self.mesh[ind1,self.ind_param['-frame w'] - 1] == 1:
                    self.mesh[ind1,self.ind_param['-frame w'] - 1] = 1
                if self.mesh[ind1,self.ind_param['frame'] + 1] - self.mesh[ind1,self.ind_param['frame']] == 1:
                    self.mesh[ind1,self.ind_param['frame']] = 1
            
            #filling in the the rest of the row`
            if ind1 + self.ind_param['slit height'] <= len(self.mesh) - self.ind_param['frame']:
                self.mesh[ind1:ind1 + self.ind_param['slit height']] = self.mesh[ind1]
                self.mesh[ind1 + self.ind_param['slit height']:ind1 + self.ind_param['pitch']] = 1
            else:
                self.mesh[ind1:self.ind_param['-frame h']] = self.mesh[ind1]
            ind1 += self.ind_param['pitch']
