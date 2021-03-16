import plotly.graph_objects as go
import math
from sympy import Symbol,sympify,diff


class Data:
    def __init__(self, vals:list):
        self.y = vals[:]
        self.mean = sum(self.y)/len(self.y)
        self.mode = None
        try:
            for i in self.y:
                if self.mode is None:
                    self.mode = i
                else:
                    if type(self.mode)==list and i in self.mode:
                        continue
                    elif (type(self.mode)==int or type(self.mode)==float) and self.mode == i:
                        continue
                    if type(self.mode)==float or type(self.mode)==int:

                        if self.y.count(i)>self.y.count(self.mode):
                            self.mode = i
                        elif self.y.count(i)==self.y.count(self.mode):
                            if type(self.mode) is not list:
                                self.mode = [self.mode]
                            self.mode.append(i)
                    else:
                        if self.y.count(i)>self.y.count(self.mode[0]):
                            self.mode = i
                        elif self.y.count(i)==self.y.count(self.mode[0]):
                            self.mode.append(i)
        except IndexError:
            self.mode = "None"
        if len(self.y)%2 == 0:
            self.median = sum(sorted(self.y)[len(self.y)//2:len(self.y)//2+2])/2
        else:
            self.median = self.y[len(self.y)//2]
        self.stDev = (sum([(i-self.mean)**2 for i in self.y])/len(self.y))**.5

    def f_showCurve(self):
        fig = go.Figure(data=[go.Histogram(x=[(i-self.mean)/self.stDev for i in self.y])])
        fig.show()

    def __repr__(self):
        res = ''
        for i in dir(self):
            if '_' in i:
                continue
            val = eval('"{i} = [self.{i}]"'.format(i=i))
            val:str
            val = val.replace('[','{')
            val = val.replace(']','}')
            res += eval(f"f\'{val}\'")+"\n"
        return res


class xyData(Data):
    def __init__(self, vals: list, x:list):
        super().__init__(vals)
        self.x = x
        self.R2 = (len(self.x)*sum([self.x[i]*self.y[i] for i in range(len(self.x))]) - sum(self.x)*sum(self.y))/ \
                  (((len(self.x)*sum([i**2 for i in self.x]))-sum(self.x)**2)*(len(self.x)*sum([i**2 for i in self.y])-sum(self.y)**2))**.5
        self.R2 = self.R2**2

    def f_LOBF(self, show=True):
        xy = {"x": self.x,
              "y": self.y,
              "logx": [math.log10(i) for i in self.x],
              "logy": [math.log10(i) for i in self.y],
              "lny": [math.log(i) for i in self.y]}

        def R_sq(x,y):
            return ((len(x)*sum(x[i]*y[i] for i in range(len(x)))-sum(x)*sum(y))/((len(x)*sum([i**2 for i in x])-sum(x)**2)*(len(x)*sum([i**2 for i in y])-sum(y)**2))**.5)**.5

        def reg(x,y):
            avg = {'x': sum(x)/len(x),
                   'y': sum(y)/len(y)}
            m = sum([(x[i]-avg['x'])*(y[i]-avg['y']) for i in range(len(x))])/sum([(i-avg['x'])**2 for i in x])
            b = avg['y'] - m * avg['x']
            return m,b

        r = {'lin':R_sq(xy['x'],xy['y']),
             'pow':R_sq(xy['logx'],xy['logy']),
             'exp':R_sq(xy['x'],xy['lny'])}
        fig = go.Figure()
        fig.add_scatter(x=xy['x'],y=xy['y'],mode='markers+text',name='Scatter')
        if r['lin'] == max(r.values()):
            m,b = reg(xy['x'],xy['y'])
            eq = f'y = {m}*x + {b}'
            fig.add_scatter(x=xy['x'],y=[m*i+b for i in xy['x']],mode='lines+text+markers',name=eq)
        elif r['pow'] == max(r.values()):
            m,b = reg(xy['logx'],xy['logy'])
            b=10**b
            eq = f'y = {b}*x^{m}'
            fig.add_scatter(x=xy['x'],y=[b*i**m for i in xy['x']],mode='lines+text+markers',name=eq)
        else:
            m,b = reg(xy['x'],xy['lny'])
            b = math.exp(b)
            eq = f'y = {b}*e^({m}*x)'
            fig.add_scatter(x=xy['x'],y=[b*math.exp(m*i) for i in xy['x']],mode='lines+text+markers',name=eq)
        if show:
            print(eq)
            fig.show()
        return eq

    def f_rate_of_change(self,x,n=15):
        try:
            assert min(self.x)<=x<=max(self.x)
        except AssertionError:
            if x > max(self.x):
                x = max(self.x)
            else:
                x = min(self.x)
            print(f'x was out of range!\nx has been set to {x}')
        y = Symbol('y')
        eq = self.f_LOBF(show=False)
        eq = eq[eq.find('=')+1:]
        eq = diff(sympify(eq.replace('x','y')))
        return eq.evalf(n=n,subs={y: x})


