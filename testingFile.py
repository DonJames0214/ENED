from ENED_ToolKit.Shape import *
from ENED_ToolKit.Figures.graph import LineGraph
import numpy as np

shape1 = Triangle(a=Side(3),b=Side(4),c=Angle(45))
x =np.linspace(.1,179.9,num=100)
y = []
for i in x:
    shape = Triangle(a=Side(3),b=Side(4),mc=Angle(i))
    y.append(shape.C)
graph = LineGraph(Triangle=[x,y])
graph.show()
