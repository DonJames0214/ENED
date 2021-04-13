class _Range:

    def __init__(self,n:int):
        self.n = n
        self.__i = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.__i += 2
        if self.__i > self.n:
            raise StopIteration
        else:
            return self.__i

    def __repr__(self):
        res = ''
        for i in self:
            if res == '':
                res = str(i)
            else:
                res += ', {i}'.format(i=i)
        return res


class Even_Range(_Range):

    def __init__(self,n):
        super(Even_Range, self).__init__(n)
        self._Range__i = -2


class Odd_Range(_Range):
    def __init__(self,n):
        super().__init__(n)
        self._Range__i = -1

