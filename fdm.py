# -*- coding: utf-8 -*-
import numpy as np
from mesh import Mesh

class FunctionSpace(object):
    """
    Пространство сеточных функций
    """
    def __init__(self, mesh, dtype=None, num_comp=1):
        """
        Констркутор пространства сеточных функций

        Parameters
        ----------
        mesh : Mesh, равномерная пространственная сетка

        num_comp : количесво компонент сеточной функции (скалярной или векторной), optional
        """
        self.mesh = mesh
        self.num_comp = num_comp
        self.dtype=dtype
        self.indices = []
        if num_comp == 1:
            self.indices = ['x'+str(i) for i in range(len(self.mesh.N))]
        else:
            self.indices = ['x'+str(i) for i in range(len(self.mesh.N))] + ['component']

    def inner(self, u, v):
        """
        Скалярное произведение по всем узлам сетки

        Parameters
        ----------
        u : сеточная функция

        v : сеточная функция

        Returns
        -------
        out : Возвращает скалярное произведение сеточных функций
        .. math:
           (u, v) = \sum_{k=1}^p \sum_{x \in \bar{\omega}_h} u_k(x) v_k(x) h
        """
        if self.num_comp == 1:
            return np.dot(u.u, v.u) * self.mesh.d[0]
        else:
            s = 0.
            for k in range(self.num_comp):
                s += np.dot(u.u[k], v.u[k]) * self.mesh.d[0]

class Function(object):
    """
    Скалярная или векторная функция.
    """
    def __init__(self, V):
        """
        Конструктор сеточной функции (элемента пространства сеточных функций)

        Parameters
        ----------
        V: FunctionSpace пространство сеточных функций
        """
        self.mesh = V.mesh
        self.num_comp = V.num_comp
        self.indices = V.indices
        self.dtype = V.dtype

        if self.num_comp == 1:
            self.u = np.zeros([self.mesh.N[i] + 1 for i in range(len(self.mesh.N))], dtype=self.dtype)
        else:
            self.u = np.zeros([self.mesh.N[i] + 1 for i in range(len(self.mesh.N))] + [self.num_comp], dtype=self.dtype)
