# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
from scipy.special import erf
from scipy.optimize import root

def T(z, t):
    Tbf, T0, Tbnd = st.session_state.problem['Tbf T0 Tbnd'.split()]
    lmbdaf = st.session_state.Soil['Conductivity']['f']
    lmbdath = st.session_state.Soil['Conductivity']['th']
    Cf = st.session_state.Soil['Capacity']['f']*1e6
    Cth = st.session_state.Soil['Capacity']['th']*1e6
    L = st.session_state.problem['L']*1e6

    def fnc(alpha):
        nom1 = lmbdaf*(Tbnd - Tbf)*np.exp(-alpha**2/(4*lmbdaf*Cf))
        denom1 = np.sqrt(lmbdaf/Cf)*erf(alpha/(2*np.sqrt(lmbdaf/Cf)))
        nom2 = lmbdath*(T0 - Tbf)*np.exp(-alpha**2/(4*lmbdath*Cth))
        denom2 = np.sqrt(lmbdath/Cth)*erf(alpha/(2*np.sqrt(lmbdath/Cth)))
        f = nom1/denom1 + nom2/denom2 + alpha*L*np.sqrt(np.pi)/2
        return f
    T = np.zeros_like(z)
    guess = 1e-3
    alpha = root(fnc,guess).x[0]
    pf = erf(alpha/(2*np.sqrt(lmbdaf/Cf)))
    pth = erf(alpha/(2*np.sqrt(lmbdath/Cth)))
    Af = Tbnd - Tbf
    Bf = -Af/pf
    Ath = (Tbf - T0)*pth/(1-pth)
    Bth = (T0 - Tbf)/(1-pth)
    for i in range(len(z)):
        Tf = Tbf + Af + Bf*erf(z[i]/np.sqrt(lmbdaf/Cf*t))
        Tth = Tbf + Ath + Bth*erf(z[i]/np.sqrt(lmbdath/Cth*t))
        zbf = alpha*np.sqrt(t)
        if z[i] < zbf:
            T[i] = Tf
        elif z[i] > zbf:
            T[i] = Tth
        else:
            T[i] = Tbf
    return zbf, T
