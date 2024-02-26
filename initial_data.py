# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 10:35:03 2023

@author: M3309200
"""

import streamlit as st
from streamlit import session_state
import pyvista as pv
from stpyvista import stpyvista
import numpy as np

## Initialize a plotter object
plotter = pv.Plotter(window_size=[400,400])
# plotter.add_axes(line_width=5, labels_off=False)
# stpyvista(plotter, horizontal_align='left')
# plotter.view_isometric()
# Sidebar components

#Data initialization - room dimensions

l = 0.0
L = 0.0
h = 0.0
L1 = 0.0
L2 = 0.0
l2 = 0.0
L3 = 0.0
l4 = 0.0
h5 = 0.0
h6 = 0.0

# LAeq calculation list initialization

lvl_table = []
source_choice = []
lvl_choice = []
lvl_list = []
data_list = []
laeq = []
laeq_glob = []
numeric_values = []
user_dnt = {}

# Dimensions initialization

if 'l' not in st.session_state:
    st.session_state['l'] = 0.0

if 'L' not in st.session_state:
    st.session_state['L'] = 0.0
    
if 'h' not in st.session_state:
    st.session_state['h'] = 0.0

if 'L1' not in st.session_state:
    st.session_state['L1'] = 0.0
    
if 'L2' not in st.session_state:
    st.session_state['L2'] = 0.0
    
if 'l2' not in st.session_state:
    st.session_state['l2'] = 0.0

if 'L3' not in st.session_state:
    st.session_state['L3'] = 0.0

if 'l4' not in st.session_state:
    st.session_state['l4'] = 0.0

if 'h5' not in st.session_state:
    st.session_state['h5'] = 0.0

if 'h6' not in st.session_state:
    st.session_state['h6'] = 0.0

# Systems initialization
    
if 'numeric_values' not in st.session_state:
    st.session_state['numeric_values'] = []

if 'user_dnt' not in st.session_state:
    st.session_state['user_dnt'] = {}

if 'material01' not in st.session_state:
    st.session_state['material01'] = ''
    
if 'lining01' not in st.session_state:
    st.session_state['lining01'] = ''
    
if 'opening01' not in st.session_state:
    st.session_state['opening01'] = ''

if 'material02' not in st.session_state:
    st.session_state['material02'] = ''
    
if 'lining02' not in st.session_state:
    st.session_state['lining02'] = ''
    
if 'opening02' not in st.session_state:
    st.session_state['opening02'] = ''    

if 'material03' not in st.session_state:
    st.session_state['material03'] = ''
    
if 'lining03' not in st.session_state:
    st.session_state['lining03'] = ''
    
if 'opening03' not in st.session_state:
    st.session_state['opening03'] = ''

if 'material04' not in st.session_state:
    st.session_state['material04'] = ''
    
if 'lining04' not in st.session_state:
    st.session_state['lining04'] = ''
    
if 'opening04' not in st.session_state:
    st.session_state['opening04'] = ''     
    
if 'material05' not in st.session_state:
    st.session_state['material05'] = ''
    
if 'lining05' not in st.session_state:
    st.session_state['lining05'] = ''
    
if 'material06' not in st.session_state:
    st.session_state['material06'] = ''
    
if 'lining06' not in st.session_state:
    st.session_state['lining06'] = ''
 
if 'room1_cb' not in st.session_state:
    st.session_state['room1_cb'] = 0    
    
if 'room2_cb' not in st.session_state:
    st.session_state['room2_cb'] = 0 
