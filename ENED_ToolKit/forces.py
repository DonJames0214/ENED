from math import sin, cos, radians, atan, sqrt, pi


class Force:

    conv = {'N':1.,'LBF':4.448,'KGF':9.807}

    def __init__(self, magnitude, direction, units="N", rad=False):
        self.mag = magnitude
        self.ang = direction
        self.units = units.upper()
        if self.units not in Force.conv:
            raise ValueError(f'"{self.units}" is not an accepted unit. Accepted units are:\n"N"\n"LBF"\n"KGF"')
        if not rad:
            self.ang = radians(self.ang)
        self.x = self.mag * cos(self.ang)
        self.y = self.mag * sin(self.ang)

    @staticmethod
    def parseXY(x, y, unit="N"):
        mag = sqrt(x ** 2 + y ** 2)
        ang = atan(y / x)
        if x < 0:
            ang += pi
        return Force(mag, ang,units=unit,rad=True)

    def __add__(self, other):
        if type(other) != type(Force(0, 0)):
            raise ValueError(f'Unsupported Addition Between A Class "force" Object And A Type "{type(other)}" object')
        other: Force
        new_x = self.x*Force.conv[self.units] + other.x*Force.conv[other.units]
        new_y = self.y*Force.conv[self.units] + other.y*Force.conv[other.units]
        return Force.parseXY(new_x/Force.conv[self.units], new_y/Force.conv[self.units],unit=self.units)

    def __repr__(self):
        return (f'Magnitude:\t{self.mag} {self.units}\n'
              f'Angle:    \t{self.ang} radians\n'
              f'x:        \t{self.x} {self.units}\n'
              f'y:        \t{self.y} {self.units}')


class _SpringSystem:

    def __init__(self,k,f,x,**kwargs):
        self.K_eq = k
        self.F_total = f
        self.X_Total = x
        for i in kwargs:
            self.__dict__[i] = kwargs[i]

    def __repr__(self):
        ind = '-' * max(len(str(i)) for i in [self.K_eq, self.F_total, self.X_Total])
        msg = \
            f'''<----------------{ind}------------->
  K equation:  {self.K_eq} N/m  
  F total   :  {self.F_total} N
  x total   :  {self.X_Total} m
            '''
        for i in self.__dict__:
            if i in ['K_eq','F_total','X_Total']:
                continue
            msg += f''' 
    <-----------{'-'*max([len(i),max([len(str(self.__dict__[i].__dict__[j])) for j in ['k','f','x']])])}--->
       Spring:  {i}
       K     :  {self.__dict__[i].k} N/m
       F     :  {self.__dict__[i].f} N
       X     :  {self.__dict__[i].x} m
    <-----------{'-'*max([len(i),max([len(str(self.__dict__[i].__dict__[j])) for j in ['k','f','x']])])}--->\n'''
        msg += f'\n<----------------{ind}------------->'
        return msg


class Spring:

    def __init__(self, k):
        self.k = k
        self.x = 0
        self.f = 0

    @staticmethod
    def comp_elong(F_total, par=False, **kwargs):
        if par:
            keq = sum([kwargs[i].k for i in kwargs])
            for i in kwargs:
                kwargs[i].x = F_total/keq
                kwargs[i].f = kwargs[i].k * kwargs[i].x
            return _SpringSystem(keq, F_total, F_total / keq,**kwargs)
        else:
            keq = (sum(1/kwargs[i].k for i in kwargs))**(-1)
            x = []
            for i in kwargs:
                kwargs[i].f = F_total
                kwargs[i].x = F_total/kwargs[i].k
                x.append(kwargs[i].x)
            return _SpringSystem(keq, F_total, sum(x), **kwargs)



