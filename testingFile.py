from ENED_ToolKit.Statics.Object import StaticObject
from ENED_ToolKit.forces import Force
obj = StaticObject(A=[Force(10,90,rad=False),2],B=[Force(10,45,rad=False),10])
obj.solve(deg=30,mag=15,)
