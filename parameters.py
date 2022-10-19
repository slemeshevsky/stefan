# -*- coding: utf-8 -*-
import numpy as np

class Parameters:
    def __init__(self):
        """
        Подклассы должны инициализировать атрибуты:
        self.prm параметрами и значениями по-умолчанию,
        self.type соответствующими типами,
        self.help соответствующими описаниями параметров.
        """
        pass

    def ok(self):
        """
        Проверяет определены ли аттрибуты prm, type и help.
        """
        if hasattr(self, 'prm') and isinstance(self.prm, dict) and \
           hasattr(self, 'type') and isinstance(self.type, dict) and \
           hasattr(self, 'help') and isinstance(self.help, dict):
            return True
        else:
            raise ValueError(f'The constructor in class {self.__class__.__name__} does not initialize the dictionaries:\n\t self.prm, self.type, self.help')

    def _illegal_parameter(self, name):
        """
        Генерирует исключение о недопустимом параметре.
        """
        raise ValueError(f'Parameter {name} is not registred. \nLegal parameters are \n{list(self.prm.keys())}')

    def set(self, **parameters):
        """
        Устанавливается один или несколько параметров.
        """
        for name in parameters:
            if name in self.prm:
                self.prm[name] = parameters[name]
            else:
                self._illegal_parameter(name)

    def get(self, name):
        """
        Возвращает значение одного или нескольких параметров.
        """
        if isinstance(name, (list, tuple)):
            for n in name:
                if n not in self.prm:
                    self._illegal_parameter(name)
            return [self.prm[n] for n in name]
        else:
            if name not in self.prm:
                self._illegal_parameter(name)
            return self.prm[name]

    def __getitem__(self, name):
        """
        Допускается доступ к параметру по индексу obj[name].
        """
        return self.get(name)

    def __setitem__(self, name, value):
        """
        Допускается задание значения параметра по индексу obj[name] = value
        """
        return self.set(name=value)

    def define_command_line_options(self, parser=None):
        self.ok()
        if parser is None:
            import argparse
            parser = argparse.ArgumentParser()

        for name in self.prm:
            tp = self.type[name] if name in self.prm else str
            help = self.help[name] if name in self.help else None
            parser.add_argument(
                '--' + name,
                default=self.get(name),
                metavar=name,
                type=tp,
                help=help
            )
        return parser

    def init_from_command_line(self, args):
        for name in self.prm:
            self.prm[name] = getattr(args, name)


class Material(Parameters):
    def __init__(self):
        self.prm = dict(Name='', Density=1000.,
                        Tbf=0.0, Wtot=0.,
                        Conductivity={'f': 2.11,'th':1.83},
                        Capacity={'f': 2.02, 'th': 2.44})
        self.type = dict(Name=str, Density=float, Tbf=float, Wtot=float,
                          Conductivity=dict, Capacity=dict)
        self.help = dict(Name='Name of material', Density='Dry density',
                         Tbf='Freezing point', Wtot='Total moisture',
                         Conductivity='Thermal conductivity:"f" - frozen state, "th" - thawed state',
                         Capacity='Volumetric heat capacity:"f" - frozen state, "th" - thawed state')

class Problem(Parameters):
    """
    Физические параметры для задачи Стефана
    """
    def __init__(self, Soil):
        self.prm = dict(H=20, M=Soil, Lw=334., T0=1.5, Tbnd=-27+273, T_end=300)
        self.prm['Tbf'] = self['M']['Tbf']
        self.prm['L'] = self['M']['Density']*self['M']['Wtot']*self['Lw']
        self.type = dict(H=float, M=Material, Lw=float, T0=float, Tbnd=float, T_end=int,
                         Tbf=self['M'].help['Tbf'], L=float)
        self.help = dict(H='Depth of soil', M='Soil material', Lw='Latent heat of freezing of water',
                         T0='Initial temperature of soil', Tbnd='Upper boundary temperature',
                         T_end='End time of simulation',
                         Tbf=self['M']['Tbf'], L='Volumetric latent heat of freezing of soil water')

    def w_u(self, T):
        A = 10.
        T = np.array([T]) if not isinstance(T, np.ndarray) else T
        return np.where(T < self['Tbf'], 1./(1 + A*(self['Tbf']-T)), 1.)

    def C(self, T):
        Cf = self['M']['Capacity']['f']
        Cth = self['M']['Capacity']['th']
        return Cf + (Cf-Cth)*self.w_u(T)

    def lmbda(self, T):
        lmbdaf = self['M']['Conductivity']['f']
        lmbdath = self['M']['Conductivity']['th']
        return lmbdaf + (lmbdaf-lmbdath)*self.w_u(T)

    def C_eff(self, T):
        w_dT = (self.w_u(T)[1:] - self.w_u(T)[:-1])/(T[1]-T[0]) if np.abs(T[1]-T[0]) > 0.0001 else np.zeros(len(T[1:]))
        w_u_dT = np.concatenate(([w_dT[0]],w_dT))
        return self.C(T) + self['L']*w_u_dT


    # def T_exact(self):

