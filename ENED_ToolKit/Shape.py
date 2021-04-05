import math

class __Shape:
    def __init__(self):
        self.perimeter = self.calc_perimeter()
        self.area = self.calc_area()

    def calc_area(self):
        pass

    def calc_perimeter(self):
        pass

    def __mul__(self, other):
        for i in self.__dict__:
            if 'm' in i or i == 'rad' or i == 'perimeter' or i == 'area':
                continue
            self.__dict__[i] *= 2
        self.perimeter = self.calc_perimeter()
        self.area = self.calc_area()
        return self


class Side:
    def __init__(self, length):
        self.length = length


class Angle:
    def __init__(self, mag, rad=False):
        if rad:
            self.mag = mag
        else:
            self.mag = math.radians(mag)


class Triangle(__Shape):
    def __init__(self, rad=False, **kwargs):
        self.rad = rad
        if len(kwargs) != 3:
            raise Exception("kwargs must have 3 inputs of at least 1 side. Instead had {0} inputs.".format(len(kwargs)))
        case = []
        adj_keys = []
        for i in kwargs:
            if isinstance(kwargs[i],Side):
                case.append('S')
                i_prime = i.upper()
                self.__dict__[i_prime] = kwargs[i].length
            elif isinstance(kwargs[i],Angle):
                case.append('A')
                if i[0] != 'm':
                    i_prime = 'm'+i.upper()
                else:
                    i_prime = i[0]+i[1:].upper()
                self.__dict__[i_prime] = kwargs[i].mag
            else:
                raise Exception('Unsupported Data Type! Must be either a Side or Angle Data Type!')
            adj_keys.append(i_prime)
        spec_case = 0
        if case.count('A')==1:
            for i in adj_keys:
                for j in adj_keys:
                    if i == j:
                        continue
                    if i in j:
                        opp = i
                        m_opp = j
                        for n in adj_keys:
                            if n != opp and n != m_opp:
                                oth = n
                        spec_case = 1
                        break
                else:
                    temp = []
                    if spec_case != 1:
                        spec_case = 2
                    for n in adj_keys:
                        if 'm' in n:
                            ang = n
                        else:
                            temp.append(n)
                    a = temp[0]
                    b = temp[1]
            if spec_case == 1:
                ind0 = 'm'+oth
                self.__dict__[ind0] = math.asin(self.__dict__[oth]*math.sin(self.__dict__[m_opp])/self.__dict__[opp])
                ind1 = 'A'
                while ind1 in adj_keys:
                    ind1 = chr(ord(ind1)+1)
                self.__dict__['m'+ind1]=math.pi-self.__dict__[m_opp]-self.__dict__[ind0]
                self.__dict__[ind1]=math.sqrt(self.__dict__[opp]**2+self.__dict__[oth]**2-
                                              2*self.__dict__[oth]*self.__dict__[opp]*math.cos(self.__dict__['m'+ind1]))
            elif spec_case == 2:
                ind0 = 'A'
                while ind0 in adj_keys:
                    ind0 = chr(ord(ind0)+1)
                self.__dict__[ind0] = math.sqrt(self.__dict__[a]**2+
                                                self.__dict__[b]**2-
                                                2*self.__dict__[a]*self.__dict__[b]*math.cos(self.__dict__[ang]))
                ind1='m'+a
                self.__dict__[ind1] = math.asin(self.__dict__[a]*math.sin(self.__dict__[ang])/self.__dict__[ind0])
                ind2='m'+b
                self.__dict__[ind2] = math.asin(self.__dict__[b]*math.sin(self.__dict__[ang])/self.__dict__[ind0])
        elif case.count('A')==2:
            spec_case = 0
            for i in adj_keys:
                for j in adj_keys:
                    if i == j:
                        continue
                    if i in j:
                        opp = i; m_opp=j
                        for n in adj_keys:
                            if n != opp and n != m_opp:
                                m_oth = n
                                break
                        spec_case = 1
                        break
            else:
                temp = []
                for i in adj_keys:
                    if 'm' in i:
                        temp.append(i)
                    else:
                        a = i
                mb = temp[0]
                mc = temp[1]
                if spec_case != 1:
                    spec_case = 2
            if spec_case==2:
                ind0 = 'm'+ a
                self.__dict__[ind0] = math.pi - self.__dict__[mb] - self.__dict__[mc]
                ind1 = mb.replace('m','')
                self.__dict__[ind1] = self.__dict__[a] * math.sin(self.__dict__[mb])/math.sin(self.__dict__[ind0])
                ind2 = mc.replace('m','')
                self.__dict__[ind2] = self.__dict__[a]*math.sin(self.__dict__[mc])/math.sin(self.__dict__[ind0])
            elif spec_case==1:
                ind0 = 'mA'
                while ind0 in adj_keys:
                    ind0 = 'm'+chr(ord(ind0[1])+1)
                self.__dict__[ind0] = math.pi - self.__dict__[m_opp] - self.__dict__[m_oth]
                ind1 = ind0.replace('m','')
                self.__dict__[ind1] = self.__dict__[opp]*math.sin(self.__dict__[ind0])/math.sin(self.__dict__[m_opp])
                ind2 = m_oth.replace('m','')
                self.__dict__[ind2] = self.__dict__[opp]*math.sin(self.__dict__[m_oth])/math.sin(self.__dict__[m_opp])
        super().__init__()

    def __repr__(self):
        res = ''
        buffer = max([len(i) for i in self.__dict__])
        for i in self.__dict__:
            temp = self.__dict__[i]
            if isinstance(temp,Side):
                temp = temp.length
            elif isinstance(temp,Angle):
                if self.rad:
                    temp = str(temp.mag)+' rad'
                else:
                    temp = str(math.degrees(temp.mag))+' deg'
            res += f'{i}{" "*(buffer - len(i))}  =  {temp}\n'
        return res

    def calc_perimeter(self):
        temp = 0
        for i in self.__dict__:
            if i == 'area' or i == 'perimeter' or i=='rad' or 'm' in i:
                continue
            temp += self.__dict__[i]
        return temp

    def calc_area(self):
        sides = []
        for i in self.__dict__:
            if i == 'area' or i == 'perimeter' or i == 'rad' or 'm' in i:
                continue
            sides.append(self.__dict__[i])
        p = self.perimeter/2
        return math.sqrt(-p*(sides[0]-p)*(sides[1]-p)*(sides[2]-p))


