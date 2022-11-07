import streamlit as st
import numpy as np
from fdm.parameters import Material, Problem
from bokeh.plotting import figure

st.title("Численное решение задачи Стефана")

def update_soil(Cf, Cth, lmbdaf, lmbdath, name, rho, Tbf, Wtot):
    Cond = dict(f=Cf, th=Cth)
    Cap = dict(f=lmbdaf, th=lmbdath)
    st.session_state.Soil.set(Name=name, Density=rho, Tbf=Tbf, Wtot=Wtot, Conductivity=Cond, Capacity=Cap)

def form_problem_params():
    if 'Soil' not in st.session_state:
        st.session_state.Soil = Material()
        st.session_state.Soil.set(Name='Песок', Density=1850, Tbf=-0.05+273, Wtot=0.2,
                                  Conductivity={'f': 2.11, 'th': 1.83},
                                  Capacity={'f': 2.02, 'th': 2.44})
    if 'problem' not in st.session_state:
        st.session_state.problem = Problem(st.session_state.Soil)
        st.session_state.problem.set(T0=1.5+273.15)
    with st.form(key='problem_data'):
        st.header(f'Параметры задачи')
        print(f"T0={st.session_state.problem['T0']}")
        T0 = st.number_input('Начальная температура материала, °C', value=st.session_state.problem['T0']-273.15)
        Tbnd = st.number_input('Температура на торце, °C', value=st.session_state.problem['Tbnd']-273.15)
        submitted1 = st.form_submit_button("Обновить")
        if submitted1:
            st.session_state.problem.set(Tbnd=Tbnd+273.15, T0=T0+273.15)
            print(f"T0={st.session_state.problem['T0']}")

def form_material_data():
    with st.form(key='material_data'):
        st.header(f'Параметры материала')
        name = st.text_input('Название материала', value=st.session_state.Soil["Name"])
        rho = st.number_input('Плотность материала, кг/м3', value=st.session_state.Soil['Density'])
        Tbf = st.number_input('Температура начала замерзания грунта, °C',value=st.session_state.Soil['Tbf']-273.15)
        Wtot = st.number_input('Общее количество влаги, д.е.', value=st.session_state.Soil['Wtot'])
        x = np.linspace(-30+273.15, 2+273.15, 100)
        with st.expander('Кривая незамерзшей воды'):
            y = st.session_state.problem.w_u(x)
            p = figure(
                title='Кривая незамерзшей воды',
                x_axis_label='Температура, °C',
                y_axis_label='Количество незамерзшей воды'
            )
            p.line(x, y, line_width=2)
            st.bokeh_chart(p, use_container_width=True)
        tab1, tab2 = st.tabs(['Теплопроводность', 'Теплоемкость'])
        with tab1:
            Cf = st.number_input('В мерзлом состоянии, Вт/(м °C)',value=st.session_state.Soil['Conductivity']['f'])
            Cth = st.number_input('В талом состоянии, Вт/(м °C)',value=st.session_state.Soil['Conductivity']['th'])
            y = st.session_state.problem.lmbda(x)
            p = figure(
                title='Зависимость теплопроводности от температуры',
                x_axis_label='Температура, °C',
                y_axis_label='Теплопроводность'
            )
            p.line(x, y, line_width=2)
            with st.expander('График'):
                st.bokeh_chart(p, use_container_width=True)
        with tab2:
            lmbdaf = st.number_input('В мерзлом состоянии, МДж/(м3 °C)',value=st.session_state.Soil['Capacity']['f'])
            lmbdath = st.number_input('В талом состоянии, МДж/(м3 °C)',value=st.session_state.Soil['Capacity']['th'])
            y = st.session_state.problem.C_eff(x)
            p = figure(
                title='Зависимость эффективной теплоемкости от температуры',
                x_axis_label='Температура, °C',
                y_axis_label='Эффективаная теплоемкость, Дж/(м3 °C)'
            )
            p.line(x, y, line_width=2)
            with st.expander('График'):
                st.bokeh_chart(p, use_container_width=True)
        submitted2 = st.form_submit_button("Обновить")
        if submitted2:
            update_soil(Cf, Cth, lmbdaf, lmbdath, name, rho, Tbf+273, Wtot)


def main_page():
    #with st.container():
    st.subheader("Постановка задачи")
    col1, col2 = st.columns([1,4])
    with col1:
        st.image("./imgs/stefan.png")
    with col2:
        st.latex(r'''
        C_{\mathrm{eff}}(T)\frac{\partial T}{\partial t} =
        \frac{\partial }{dz} \left( \lambda(T) \frac{\partial T}{\partial z} \right)
        ''')
        st.latex(r'''
        T(x,0) = T_0
        ''')
        st.latex(r'''
        T(0, t) = T_{\mathrm{bnd}}, \quad q = k(T)\frac{\partial T(l, t)}{\partial x} = 0
        ''')
        st.latex(r'''
        C_{\mathrm{eff}}(T) = C(T) + L\frac{dw_u}{dT}(T), \quad L = \rho W_{\mathrm{tot}}L_w,
        ''')
        st.latex(r'''
        C(T) = C_f + (C_{th} - C_f) w_u(T)
        ''')
        st.latex(r'''
        \lambda(T) = \lambda_f + (\lambda_{th} - \lambda_f) w_u(T)
        ''')
        st.write('''Здесь $C{\mathrm{eff}}(T)$ --- объемная эффективная теплоемкость, $C(T)$ --- объемная теплоемкость, $\lambda(T)$ --- теплопроводность,
        $w_u(T)$ --- отношение количества незамерзшей воды к общему количеству влаги, $L_w=334$ kДж/кг''')
        #with st.expander("Параметры задачи"):

        form_problem_params()
        form_material_data()


