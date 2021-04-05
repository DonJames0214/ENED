from ENED_ToolKit.forces import Force
from math import asin,sin,radians,sqrt


class StaticObject:

    def __init__(self,axis='y',**kwargs):
        self.x_moments = {}
        self.y_moments = {}
        for i in kwargs:
            # inputs must be a size 2 list with the first value being a
            # force object while the second2 value is the distance from the axis of rotation
            try:
                assert type(kwargs[i]) == list and len(kwargs[i]) == 2
            except AssertionError:
                raise Exception('Inputs for a static object must be a list of size 2\nWith the first value being'
                                ' a force object while the second value \nIs the distance from the axis of rotation')
            kwargs[i][0]: type(Force(0,0))
            self.x_moments[i] = kwargs[i][0].X_Total * kwargs[i][1]
            self.y_moments[i] = kwargs[i][0].y*kwargs[i][1]
        self.delta_force = Force(0,0)
        for i in kwargs.values():
            self.delta_force += i[0]
        if axis.lower() == 'x':
            for i in self.x_moments:
                self.__dict__[f'{i}_moment'] = self.x_moments[i]
        else:
            for i in self.y_moments:
                self.__dict__[f'{i}_moment'] = self.y_moments[i]
            axis = 'y'
        self.axis = axis.lower()




