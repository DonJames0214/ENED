from plotly.subplots import make_subplots
from plotly.io import templates
import plotly.graph_objects as go

templates.default = 'plotly_dark'


def lineGraph(x: list, y: list, mode="lines+text", x_axis="x-axis", y_axis='y-axis'):
    fig = make_subplots(rows=1, cols=1, x_title=x_axis, y_title=y_axis)
    fig.add_scatter(x=x, y=y, mode=mode)
    fig.show()


def barChart(values:dict, x_axis="",y_axis=""):
    fig = make_subplots(rows=1,cols=1,x_title=x_axis,y_title=y_axis)
    fig.add_trace(go.Bar(x=[i for i in values],y=[values[i]for i in values]))
    fig.show()


def PieChart(values:dict,title=None):
    fig = go.Figure(data=go.Pie(labels=[i for i in values],values=[values[i] for i in values],title=title))
    fig.show()


class _Figure:

    def __init__(self):
        self.fig = go.Figure()

    def show(self):
        global templates
        self.fig.show()
        templates.default = 'plotly_dark'


class LineGraph(_Figure):

    def __init__(self, **kwargs):
        super().__init__()
        self._lines = {}
        for i in kwargs:
            self._lines[i] = kwargs[i]
            self.fig.add_scatter(x=kwargs[i][0],y=kwargs[i][1],mode='lines+text',name=i)

    def __add__(self, other):
        other: LineGraph()
        new_lines = {}
        for i in self._lines:
            new_lines[i] = self._lines[i]
        for j in other._lines:
            if j in new_lines:
                print(f'Repeated instances of "{j}" found!\n"{j}" has been overwritten with latest value!\n{new_lines}')
            new_lines[j] = other._lines[j]
        return LineGraph(**new_lines)
