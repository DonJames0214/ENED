from math import sin, cos, radians, atan, sqrt


class Force:

    conv = {'N':1.,'LBF':4.448,'KGF':9.807}

    def __init__(self, magnitude, direction, units="N", rad=True):
        self.mag = magnitude
        self.ang = direction
        self.units = units.upper()
        if self.units not in Force.conv:
            raise ValueError(f'"{self.units}" is not an accepted unit. Accepted units are:\n"N"\n"LBF"\n"KGF"')
        if not rad:
            self.ang = radians(self.ang)
        self.x = self.mag * cos(self.ang)
        self.y = self.mag * sin(self.ang)

    @classmethod
    def parseXY(cls, x, y, unit="N"):
        mag = sqrt(x ** 2 + y ** 2)
        ang = atan(y / x)
        return Force(mag, ang,units=unit)

    def __add__(self, other):
        if type(other) != type(Force(0, 0)):
            raise ValueError(f'Unsupported Addition Between A Class "force" Object And A Type "{type(other)}" object')
        other: Force
        new_x = self.x*Force.conv[self.units] + other.x*Force.conv[other.units]
        new_y = self.y*Force.conv[self.units] + other.y*Force.conv[other.units]
        return Force.parseXY(new_x/Force.conv[self.units], new_y/Force.conv[self.units],unit=self.units)

    def print(self):
        print(f'Magnitude:\t{self.mag} {self.units}\n'
              f'Angle:    \t{self.ang} radians\n'
              f'x:        \t{self.x} {self.units}\n'
              f'y:        \t{self.y} {self.units}')
