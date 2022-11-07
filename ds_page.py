# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import mpld3
import streamlit as st
import time
from exact import T
import streamlit.components.v1 as components

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
        if 'sol_plot' not in st.session_state:
            st.session_state.sol_plot = st.empty()
 #       st.header("Результаты")
        if submitted:
            st.session_state.my_bar.progress(0)
            dt *= 86400
            T_end *= 86400
            st.session_state.zbf, st.session_state.res = exact_solution(dx, dt, T_end=T_end)
  #          print(f'zbf={st.session_state.zbf}')

def description():
    col1, col2 = st.columns([3,2])
    with col1:
        st.latex(r'''
        c_i \frac{T_i^{j+1} - T_i^j}{\tau} = \frac{1}{h^2} \left( a_{i+1/2} \left( T_{i+1}^j - T_{i}^j \right) - a_{i-1/2} \left( T_{i}^j - T_{i-1}^j \right) \right),
        ''')
        st.latex(r'''
        c_i = C_{\mathrm{eff}}(T_{i}^j), \quad
        a_{i+1/2} = 0.5 (\lambda(T_{i+1}^j) + \lambda(T_{i}^j)),
        ''')
        st.latex(r'''
        T_i^0 = T_0, \quad
        i = 1, 2, \ldots, N-1,
        ''')
        st.latex(r'''
        T_0^{j+1} = T_{\mathrm{bnd}}, \quad
        a_{N+1/2} \frac{T_{N+1}^{j} - T_{N-1}^{j}}{h} = 0,\quad j = 0, 1, \ldots, M,
        ''')
        st.write('Выражаем значение на следующем временном шаге $T_i^{n+1}$')
        st.latex(r'''
        T_i^{j+1} = T_i^j + \frac{\tau}{c_i h^2} \left( a_{i+1/2} \left( T_{i+1}^j - T_{i}^j \right) - a_{i-1/2} \left( T_{i}^j - T_{i-1}^j \right) \right), \quad i = 1, 2, \ldots, N-1,
        ''')
        #
        st.latex(r'''
        T_0^{j+1} = T_{\mathrm{bnd}}, \quad
        T_N^{j+1} = T_N^j - \frac{\tau}{c_N h^2} \left( \lambda(T_{N-1}^j) \left( T_{N-1}^j - T_{N}^j \right) \right), 
        ''')
    with col2:
        st.image('./imgs/time-space-grid.png')

def exact_solution(dx, dt, T_end=20):
    st.session_state.my_bar.progress(0)
    z = np.linspace(0, st.session_state.problem['H'], int(st.session_state.problem['H']/dx)+1)
    t = 0
    time_interval = [0]
    zbfs = [0]
    res = [T(z,0)]
    fig, ax = plt.subplots(figsize=(3,1.5))
    ax.set_xlabel('Глубина, м')
    ax.set_ylabel('Температура, К')
    print(f'z={z}, T(z,0) = {res[0][1]}')
    plotLine, = ax.plot(z, res[0][1])
    plotTitle = ax.set_title('t = 0')
    fig_html = mpld3.fig_to_html(fig)
    # with st.session_state.sol_plot.container():
    #     st.pyplot(fig)
    day=0
    rem_t = float(T_end)
    while t < T_end:
        rem_t = T_end - t
        dt = dt if rem_t > dt else rem_t
        t += dt
        day = int(t/86400)
        u = np.zeros_like(z)
        zbf, u = T(z, t)
        time_interval.append(t)
        zbfs.append(zbf)
        time.sleep(0.05)
        with st.session_state.placeholder.container():
            st.header('Результаты')
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label='День',
                    value=day)
                st.metric(
                    label='Глубина промерзания, м',
                    value=zbf
                )
            with col2:
                with st.session_state.sol_plot.container():
                    plotLine.set_ydata(u)
                    plotTitle.set_text(f'{t/86400} день')
#                    components.html(fig_html, height=300)
                    st.pyplot(fig)

        
        res.append(u)
        st.session_state.my_bar.progress(t/T_end)
    return zbfs, res

def ds_page():
    #print(f'session_state_here={st.session_state}')
    st.title('Разностная схема')
    #print(f'problem={st.session_state.problem.prm},\n soil={st.session_state.Soil.prm}')
    description()
    form_grid_data()
#    print(f'session_state_and_here={st.session_state}')
#    form_viz_data()

