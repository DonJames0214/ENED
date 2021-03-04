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
