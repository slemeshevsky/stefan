# -*- coding: utf-8 -*-
import numpy as np

class Mesh(object):
    """
    Равномерная сетка на гиперкубе в n-мерном пространстве.

    Атрибуты
    --------

    x: list
       Координаты узлов сетки
    L: list
       Либо список, либо список списков с минимальными и максимальными координатами в каждом направлении
    N: list или int
       Количество отрезков по каждому направлению
    d: list или float
       Шаги по каждому направлению

    Свойства
    --------
    space_dim: int
       Размерность пространства
    """

    def __init__(self, L=None, N=None, d=None):
        """
        Конструктор сетки.

        Аргументы
        ---------
        L: list
           Либо список, либо список списков с минимальными и максимальными координатами в каждом направлении
        N: list или int
           Количество отрезков по каждому направлению
        d: list или float
           Шаги по каждому направлению
        Либо N либо d должны быть заданы
        """


        if N is None and d is None:
            raise ValueError("Mesh constructor: either N either d must be given")
        if L is None:
            raise ValueError("Mesh constructor: L must be given")

        if L is not None and isinstance(L[0], (float, int)):
            L = [L]
        if N is not None and isinstance(N, (float, int)):
            N = [N]
        if d is not None and isinstance(d, (float, int)):
            d = [d]

        self.x = None
        self.N = None
        self.d = None

        if N is None and d is not None and L is not None:
            self.L = L

            if len(d) != len(L):
                raise ValueError(f'd has different size (no of spce dim.) from L: {len(d)} vs {len(L)}')
            self.d = d
            self.N = [int(round(float(self.L[i][1] - self.L[i][0])/d[i])) for i in range(len(d))]

        if d is None and N is not None and L is not None:
            self.L = L
            if len(N) != len(L):
                raise ValueError(f'N has different size (no of spce dim.) from L: {len(N)} vs {len(L)}')
            self.N = N
            self.d = [float(self.L[i][1] - self.L[i][0])/N[i] for i in range(len(N))]

        if self.N is not None:
            self.x = [np.linspace(self.L[i][0], self.L[i][1], self.N[i]+1) for i in range(len(self.L))]


    @property
    def space_dim(self):
        return len(self.d) if self.d is not None else 0
