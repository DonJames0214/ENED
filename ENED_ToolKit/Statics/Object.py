from ENED_ToolKit.forces import Force


class StaticObject:

    def __init__(self,axis='y',**kwargs):
        x_moments = {}
        y_moments = {}
        for i in kwargs:
            # inputs must be a size 2 list with the first value being a
            # force object while the second2 value is the distance from the axis of rotation
            try:
                assert type(kwargs[i]) == list and len(kwargs[i]) == 2
            except AssertionError:
                raise Exception('Inputs for a static object must be a list of size 2\nWith the first value being'
                                ' a force object while the second value \nIs the distance from the axis of rotation')
            kwargs[i][0]: type(Force(0,0))
            x_moments[i] = kwargs[i][0].x*kwargs[i][1]
            y_moments[i] = kwargs[i][0].y*kwargs[i][1]
        self.delta_force = Force(0,0)
        for i in kwargs.values():
            self.delta_force += i[0]
        if axis.lower() == 'x':
            for i in x_moments:
                self.__dict__[f'{i}_moment'] = x_moments[i]
        else:
            for i in y_moments:
                self.__dict__[f'{i}_moment'] = y_moments[i]

    def solve(self,**kwargs):
        accepted_key = ['x','y','type','deg','mag']
        for i in kwargs.keys():
            try:
                assert i in accepted_key
            except AssertionError:
                raise ValueError(f'{i} is not a valid keyword. Accepted keywords are shown here:\n{accepted_key}')


