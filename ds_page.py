# -*- coding: utf-8 -*-

import streamlit as st
from exact import exact_solution

def form_grid_data():
    with st.form(key="grid_data"):
        st.header('Параметры сетки')
        dx = st.number_input('Шаг сетки по пространству, м', value=1)
        dt = st.number_input('Шаг сетки по времени, дни', value=1)
        #t = 0
        #time_interval = []
        zbf = []
        #res = []
        # Hbf = st.metric("Глубина промерзания, м", value=zbf)
        if 'zbf' not in st.session_state:
            st.session_state.zbf=zbf
        T_end = st.number_input('Время окончания расчета, дни', value=st.session_state.problem['T_end'])
        submitted = st.form_submit_button('Расчитать')
        if 'my_bar' not in st.session_state:
            st.session_state.my_bar = st.progress(0)
        if 'placeholder' not in st.session_state:
            st.session_state.placeholder = st.empty()
 #       st.header("Результаты")
        if submitted:
            st.session_state.my_bar.progress(0)
            dt *= 86400
            T_end *= 86400
            st.session_state.zbf, st.session_state.res = exact_solution(dx, dt, T_end=T_end)
  #          print(f'zbf={st.session_state.zbf}')

#def form_viz_data():

def description():
    col1, col2 = st.columns([3,2])
    with col1:
        st.latex(r'''
        c_i \frac{T_i^{n+1} - T_i^n}{\tau} = \frac{1}{h^2} \left( a_{i+1/2} \left( T_{i+1}^n - T_{i}^n \right) - a_{i-1/2} \left( T_{i}^n - T_{i-1}^n \right) \right),
        ''')
        st.latex(r'''
        c_i = C_{\mathrm{eff}}(T_{i}^n), \quad
        a_{i+1/2} = 0.5 (\lambda(T_{i+1}^n) + \lambda(T_{i}^n)),
        ''')
        st.latex(r'''
        T_i^0 = T_0, \quad
        i = 1, 2, \ldots, N-1,
        ''')
        st.latex(r'''
        T_0^{n+1} = T_{\mathrm{bnd}}, \quad
        a_{N+1/2} \frac{T_{N+1}^{n} - T_{N-1}^{n}}{h} = 0,\quad n = 0, 1, \ldots, M,
        ''')
        st.write('Выражаем значение на следующем временном шаге $T_i^{n+1}$')
        st.latex(r'''
        T_i^{n+1} = T_i^n + \frac{\tau}{c_i h^2} \left( a_{i+1/2} \left( T_{i+1}^n - T_{i}^n \right) - a_{i-1/2} \left( T_{i}^n - T_{i-1}^n \right) \right), \quad i = 1, 2, \ldots, N-1,
        ''')
        #
        st.latex(r'''
        T_0^{n+1} = T_{\mathrm{bnd}}, \quad
        T_N^{n+1} = T_N^n - \frac{\tau}{c_N h^2} \left( \lambda(T_{N-1}^n) \left( T_{N-1}^n - T_{N}^n \right) \right), 
        ''')
    with col2:
        st.image('./imgs/time-space-grid.png')


def ds_page():
    #print(f'session_state_here={st.session_state}')
    st.title('Разностная схема')
    #print(f'problem={st.session_state.problem.prm},\n soil={st.session_state.Soil.prm}')
    description()
    form_grid_data()
#    print(f'session_state_and_here={st.session_state}')
#    form_viz_data()

