import pandas as pd


class Trace:

    def __init__(self,header, fun,*args):
        self.dict = {}
        self.vals = [i for i in fun(*args)]
        ind = 0
        for i in header:
            self.dict[i]=[j[ind] for j in self.vals]
            ind += 1
        self.df = pd.DataFrame(data=self.dict)
