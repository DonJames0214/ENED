import plotly.graph_objects as go
import math
import pandas as pd


class Data:
    ignore_var = []

    def __init__(self, vals: list):
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
            if '_' in i or i in self.ignore_var:
                continue
            val = eval('"{i} = [self.{i}]"'.format(i=i))
            val: str
            val = val.replace('[','{')
            val = val.replace(']','}')
            res += eval(f"f\'{val}\'")+"\n"
        return res


class xyData(Data):
    ignore_var = ['df','sqErr']

    def __init__(self, vals: list, x:list):
        super().__init__(vals)
        self.x = x
        self.R2 = (len(self.x)*sum([self.x[i]*self.y[i] for i in range(len(self.x))]) - sum(self.x)*sum(self.y))/ \
                  (((len(self.x)*sum([i**2 for i in self.x]))-sum(self.x)**2)*(len(self.x)*sum([i**2 for i in self.y])-sum(self.y)**2))**.5
        self.R2 = self.R2**2
        self.df = None
        self.sqErr = None

    def f_lobf(self):
        xy = {"x": self.x,
              "y": self.y,
              "logx": [math.log10(i) for i in filter(lambda x:x!=0, self.x)],
              "logy": [math.log10(i) for i in filter(lambda x:x!=0,self.y)],
              "lny": [math.log(i) for i in filter(lambda x:x!=0,self.y)]}

        def R_sq(x,y):
            return ((len(x)*sum(x[i]*y[i] for i in range(len(x)))-sum(x)*sum(y))/((len(x)*sum([i**2 for i in x])-sum(x)**2)*(len(x)*sum([i**2 for i in y])-sum(y)**2))**.5)**.5

        def reg(x,y):
            avg = {'x': sum(x)/len(x),
                   'y': sum(y)/len(y)}
            m = sum([(x[i]-avg['x'])*(y[i]-avg['y']) for i in range(len(x))])/sum([(i-avg['x'])**2 for i in x])
            b = avg['y'] - m * avg['x']
            return m,b
        yind = None
        if 0 in xy['x']:
            if 0 in xy['y']:
                if xy['y'].index(0) == xy['x'].index(0):
                    pass
                else:
                    del xy['logx'][xy['y'].index(0)]
                    del xy['logy'][xy['x'].index(0)]
            else:
                del xy['logy'][xy['x'].index(0)]

        if 0 in xy['y']:
            yind = xy['y'].index(0)
            if len(xy['y'])==len(xy['logx']):
                del xy['logx'][xy['y'].index(0)]




        r = {'lin':R_sq(xy['x'],xy['y']),
             'pow':R_sq(xy['logx'],xy['logy'])}
        if yind is not None:
            r['exp'] = R_sq([i for i in filter(lambda x:x!=xy['x'][yind],xy['x'])],xy['lny'])
        else:
            r['exp'] = R_sq(xy['x'],xy['lny'])
        fig = go.Figure()
        fig.add_scatter(x=xy['x'],y=xy['y'],mode='markers+text',name='Scatter')
        fun = lambda x:None
        try:
            if r['lin'] == max(r.values()):
                m,b = reg(xy['x'],xy['y'])
                eq = f'y = {m}*x + {b}'
                fig.add_scatter(x=xy['x'],y=(yp:=[m*i+b for i in xy['x']]),mode='lines+text+markers',name=eq)
                fun = lambda x:m*x+b
            elif r['pow'] == max(r.values()):
                m,b = reg(xy['logx'],xy['logy'])
                b=10**b
                eq = f'y = {b}*x^{m}'
                fig.add_scatter(x=xy['x'],y=(yp:=[b*i**m for i in xy['x']]),mode='lines+text+markers',name=eq)
                fun = lambda x:b*x**m
            else:
                m,b = reg(xy['x'],xy['lny'])
                b = math.exp(b)
                eq = f'y = {b}*e^({m}*x)'
                fig.add_scatter(x=xy['x'],y=(yp:=[b*math.exp(m*i) for i in xy['x']]),mode='lines+text+markers',name=eq)
                fun = lambda x:b*math.exp(m*x)
        except TypeError:
            try:
                if r['pow'] == max(r.values()):
                    m, b = reg(xy['logx'], xy['logy'])
                    b = 10 ** b
                    eq = f'y = {b}*x^{m}'
                    fig.add_scatter(x=xy['x'], y=(yp := [b * i ** m for i in xy['x']]), mode='lines+text+markers', name=eq)
                    fun = lambda x: b * x ** m
                else:
                    m, b = reg(xy['x'], xy['lny'])
                    b = math.exp(b)
                    eq = f'y = {b}*e^({m}*x)'
                    fig.add_scatter(x=xy['x'], y=(yp := [b * math.exp(m * i) for i in xy['x']]), mode='lines+text+markers',
                                    name=eq)
                    fun = lambda x: b * math.exp(m * x)
            except TypeError:
                m, b = reg(xy['x'], xy['lny'])
                b = math.exp(b)
                eq = f'y = {b}*e^({m}*x)'
                fig.add_scatter(x=xy['x'], y=(yp := [b * math.exp(m * i) for i in xy['x']]), mode='lines+text+markers',
                                name=eq)
                fun = lambda x: b * math.exp(m * x)
        print(eq)
        print(len(yp),len(xy['x']),len(xy['y']),sep='----')
        self.df = pd.DataFrame(data={"x": xy['x'],
                                     "y": xy['y'],
                                     "yp": yp,
                                     "y - yp": [xy['y'][i]-yp[i] for i in range(len(yp))],
                                     "(y - yp)^2": [(xy['y'][i]-yp[i])**2 for i in range(len(yp))]})
        self.sqErr = sum(self.df['(y - yp)^2'])
        fig.show()
        return fun
