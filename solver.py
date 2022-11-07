# -*- coding: utf-8 -*-

import numpy as np
from mesh import Mesh
from parameters import Material, Parameters, Problem
from fdm import FunctionSpace, Function

class Solver(Parameters):
    def __init__(self, problem):
        "docstring"
        self.problem = problem
        self.prm = dict(D=0.5, Nx=3, stability_safety_factor=1.0)
        self.type = dict(D=float, Nx=int, stability_safety_factor=float)
        self.help = dict(D='"Fourier" number',
                         Nx='Number of spatial points',
                         stability_safety_factor='Stability factor')
        L_end = self.problem['H']
        dx = L_end/float(self['Nx'])
        self.m = Mesh(L=[0,L_end], d=[dx])
        t_interval = self.problem['T_end']
        self.dt = self['D']*dx**2*24*3600
        V = FunctionSpace(self.m)
        self.f = Function(V)

    def set(self, **parameters):
        super().set(**parameters)
        dx = self.problem['H']/float(self['Nx'])
        self.m = Mesh(L=[0, self.problem['H']], d=[dx])
        self.dt = self['D']*dx**2*24*3600
        V = FunctionSpace(self.m)
        self.f = Function(V)

    def solve(self):
        L_end, T_end = self.problem['H T_end'.split()]
        D, Nx, stability_safety_factor = self['D Nx stability_safety_factor'.split()]
        dx = self.m.d[0]
        #self.dt = D*dx**2
        I = self.problem['T0']
       
        U_0 = self.problem['Tbnd']
        x = np.linspace(0, self.problem['H'], Nx+1)
        dx = x[1] - x[0]
        
        u = np.zeros(Nx+1)
        u_n = np.zeros(Nx+1)

        for i in range(0,Nx+1):
            u_n[i] = I

        a = self.problem.lmbda(u_n)
        c = self.problem.C_eff(u_n)
        self.dt = D*s.m.d[0]**2/(np.max(a/c))
        print(f'dt={self.dt}')
        t = self.dt
        dt = self.dt
        gamma = dt/s.m.d[0]**2

        while(t < self.problem['T_end']):
            u[1:-1] = u_n[1:-1] + gamma/2.*((a[2:]+a[1:-1])/c[1:-1]*(u_n[2:] - u_n[1:-1]) +
                                            (a[1:-1]+a[0:-2])/c[1:-1]*(u_n[1:-1] - u_n[:-2]))
            u[0] = U_0
            u[-1] = u_n[-1] - 2*gamma*a[-1]/c[-1]*(u_n[-1] - u_n[-2])
            u_n[:] = u

            a = self.problem.lmbda(u_n)
            c = self.problem.C_eff(u_n)
            remaining_t = self.problem['T_end'] - t
            self.dt = D*s.m.d[0]**2/(np.max(a/c))
            dt = self.dt if remaining_t > self.dt else remaining_t
            print(f'dt={self.dt}')
            t += dt
            gamma = dt/s.m.d[0]**2
#            print(f't={t}, dt={self.dt}, rem_t={remaining_t}')
        return x, u


if __name__ == '__main__':
    Soil = Material()
    Soil.set(Name='Песок', Density=1850, Tbf=-0.05, Wtot=0.2,
             Conductivity={'f': 2.11, 'th': 1.83},
             Capacity={'f': 2.02e6, 'th': 2.44e6}
             )
    problem = Problem(Soil)
    s = Solver(problem)
    s.set(Nx=50)
    s.problem.set(T0=1.5+273.15, T_end=s.dt*10000)
    x, y = s.solve()
