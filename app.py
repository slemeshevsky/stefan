# -*- coding: utf-8 -*-

import streamlit as st
st.set_page_config(layout='wide')

from problem_page import main_page
from ds_page import ds_page

st.sidebar.title("Навигация")
options = st.sidebar.radio("", options=['Задача', 'Разностная схема'])

#main_page()
if options == 'Разностная схема':
    ds_page()
else:
    main_page()

