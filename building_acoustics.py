# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 09:58:36 2023

@author: M3309200
"""


import initial_data
import acoustic_data
import pyvista as pv
import numpy as np
import streamlit as st
import subprocess
import ast
from streamlit import session_state
from stpyvista import stpyvista
from acoustic_data import *
from streamlit_extras.row import row
from streamlit_extras.grid import grid
import matplotlib.pyplot as plt
from matplotlib import ticker
from acoustics import building

# Set page configuration
st.set_page_config(
    page_title="Building acoustics",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# ipythreejs does not support scalar bars :(
pv.global_theme.show_scalar_bar = True

## Initialize a plotter object
# Create a plotter with a specific size
plotter = pv.Plotter(window_size=[600, 400])
plotter.background_color = (0.9, 0.9, 0.9)

# Set the CSS style to adjust the width of the plotter
st.markdown(
    """
    <style>
        .css-1aumxhk {
            max-width: 50%;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# material_library = st.sidebar.file_uploader("Material library")

st.sidebar.write ('Room')
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.session_state.l = st.number_input('l', value = st.session_state.l, step=1.,format="%.2f")
with col2:
    st.session_state.L = st.number_input('L', value = st.session_state.L, step=1.,format="%.2f")
with col3:
    st.session_state.h = st.number_input('h', value = st.session_state.h, step=1.,format="%.2f")

####Adjacent rooms parameters definition

def plot3droom(cx,cy,cz, l, L, h, color_r,color_g,color_b,leg=None):
    plotter.add_axes(line_width=5)
    vertices = np.array([[cx,cy,cz],[cx,cy+L,cz],[cx+l,cy+L,cz],[cx+l,cy,cz],[cx,cy,cz+h],[cx,cy+L,cz+h],[cx+l,cy+L,cz+h],[cx+l,cy,cz+h]])
    faces = np.hstack([[4,0,1,2,3],[4,0,4,7,3],[4,0,4,5,1],[4,1,5,6,2],[4,3,7,6,2],[4,4,5,6,7]])
    mesh = pv.PolyData(vertices, faces)
    mesh.cell_data['colors'] = [[color_r,color_g,color_b],[color_r,color_g,color_b],[color_r,color_g,color_b],[color_r,color_g,color_b],[color_r,color_g,color_b],[color_r,color_g,color_b]]
    plotter.add_mesh(mesh,scalars='colors',rgb=True)
    return

center_col1, center_col2 = st.columns(2)

with center_col1:
    #Plot Reception room = Room
    if st.session_state.l != 0 and st.session_state.L != 0 and st.session_state.h != 0:
        plot3droom(0,0,0,st.session_state.l, st.session_state.L, st.session_state.h, 85, 240, 158,'Room')
    
    room_choice = st.sidebar.radio("Emission room choice",["Adjacent","Exterior"])
    
    #Plot Adjacent
    if room_choice == "Adjacent":
        col1, col2 = st.sidebar.columns(2)
        with col2:
            st.session_state.L2 = st.number_input("L2", value = st.session_state.L2,step=1.,format="%.2f")
        if st.session_state.L2 != 0:
            plot3droom(0,-st.session_state.L2,0,st.session_state.l,st.session_state.L2, st.session_state.h, 118,118,118,'Room1')
    
    #Plot Facade
    if room_choice == "Exterior":
        if st.session_state.L2 != 0:
            plot3droom(st.session_state.l,0,0,0,st.session_state.L, st.session_state.h, 0,0,255,'Facade1')            
 

    ## Final touches
    plotter.view_isometric()
    
    ## Send to streamlit
    stpyvista(plotter, horizontal_align='left')


with center_col1:
    st.write("Performances visualizer")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Materials", "Doublings", "Openings", "Air inlets","Roller shutter boxes"])
    
    with tab1:    
        rcol1, rcol2, rcol3 = st.columns(3)
        with rcol1:
            options = st.multiselect("Materials",materials)
        fig, ax = plt.subplots()  
        for i, selection in enumerate(options):
            ax.plot(freq, eval(selection).sri, label = selection)
            st.text(selection + ' : Rw(C;Ctr) = %d(-%d;-%d) '% (building.rw(eval(selection).sri[3:19]),building.rw(eval(selection).sri[3:19])-building.rw_c(eval(selection).sri[3:19]),building.rw(eval(selection).sri[3:19])-building.rw_ctr(eval(selection).sri[3:19])))
        ax.set_xscale('log')
        ax.set_xticks(freq)
        ax.get_xaxis().set_major_formatter(plt.FixedFormatter(freq))
        ax.get_xaxis().set_tick_params(which='minor', size=0)
        ax.get_xaxis().set_tick_params(which='minor', width=0) 
        ax.tick_params(axis='x', rotation=90)
        ax.grid(which = "major")
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Sound reduction index (dB)')
        ax.set_title('Performance for selected materials')
        ax.legend()
        st.pyplot(fig)
        # for j, selection2 in enumerate (options2):
        #     ax.plot(freq, eval(selection2).d_sri, label = selection2)
        #     st.pyplot(fig)
            # if (materials in options2):
            #     # for k in range(len(freq)):
            #     #     curve = 
            #     ax.plot(freq, eval(materials).sri + eval(selection2).d_sri)

    with tab2:    
        rcol1, rcol2, rcol3 = st.columns(3)
        with rcol1:
            options = st.multiselect("Doublings",linings)
        fig, ax = plt.subplots()  
        for i, selection in enumerate(options):
            ax.plot(freq, eval(selection).d_sri, label = selection)
            # st.text(selection + ' : Rw(C;Ctr) = %d(-%d;-%d) '% (building.rw(eval(selection).sri[3:19]),building.rw(eval(selection).sri[3:19])-building.rw_c(eval(selection).sri[3:19]),building.rw(eval(selection).sri[3:19])-building.rw_ctr(eval(selection).sri[3:19])))
        ax.set_xscale('log')
        ax.set_xticks(freq)
        ax.get_xaxis().set_major_formatter(plt.FixedFormatter(freq))
        ax.get_xaxis().set_tick_params(which='minor', size=0)
        ax.get_xaxis().set_tick_params(which='minor', width=0) 
        ax.tick_params(axis='x', rotation=90)
        ax.grid(which = "major")
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Sound reduction index (dB)')
        ax.set_title('Performance for selected materials')
        ax.legend()
        st.pyplot(fig)       
       
    with tab3:
        options = st.multiselect("Openings",openings)
        # st.text(options)
        fig, ax = plt.subplots()
        for selection in options:
            ax.plot(freq, eval(selection).sri, label = selection)
            st.text(selection + ' : Rw(C;Ctr) = %d(-%d;-%d) '% (building.rw(eval(selection).sri[3:19]),building.rw(eval(selection).sri[3:19])-building.rw_c(eval(selection).sri[3:19]),building.rw(eval(selection).sri[3:19])-building.rw_ctr(eval(selection).sri[3:19])))
        ax.set_xscale('log')
        ax.set_xticks(freq)
        ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
        ax.get_xaxis().set_tick_params(which='minor', size=0)
        ax.get_xaxis().set_tick_params(which='minor', width=0) 
        ax.tick_params(axis='x', rotation=90)
        ax.grid(which = "major")    
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Sound reduction index (dB)')
        ax.set_title('Performance for selected materials')
        ax.legend()
        st.pyplot(fig)
        
        
    with tab4:
        options = st.multiselect("Air inlets",air_inlets)
        fig, ax = plt.subplots()
        for i, selection in enumerate(options):
            ax.plot(freq, eval(selection).n_sri, label = selection)
        ax.set_xscale('log')
        ax.set_xticks(freq)
        ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
        ax.get_xaxis().set_tick_params(which='minor', size=0)
        ax.get_xaxis().set_tick_params(which='minor', width=0) 
        ax.tick_params(axis='x', rotation=90)
        ax.grid(which = "major")
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Normalized sound reduction index (dB)')
        ax.set_title('Performance for selected materials')
        ax.legend()
        st.pyplot(fig)
         
    with tab5:
        options = st.multiselect("Roller shutter boxes",roller_shutter_boxes)    

        fig, ax = plt.subplots()
        for i, selection in enumerate(options):
            ax.plot(freq, eval(selection).n_sri, label = selection)
        ax.set_xscale('log')
        ax.set_xticks(freq)
        ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
        ax.get_xaxis().set_tick_params(which='minor', size=0)
        ax.get_xaxis().set_tick_params(which='minor', width=0) 
        ax.tick_params(axis='x', rotation=90)
        ax.grid(which = "major")
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Normalized sound reduction index (dB)')
        ax.set_title('Performance for selected materials')
        ax.legend()
        st.pyplot(fig)
    

with center_col2:
    
    if room_choice == "Exterior":
        st.write('Facade')
        grid3 = grid([1],[1],[2, 3,3],[1],[1],vertical_align="bottom")
        materialfa = grid3.selectbox('Facade',materials, key = "materialfa")
        liningfa1 = grid3.selectbox('Doubling',linings, key = "liningfa1")
        openingfa = grid3.selectbox('Openings',openings, key = "openingfa")
        grid3.number_input("l_op_fa", value = 1.0, key = "l_op_fa")
        grid3.number_input("h_op_fa", value = 1.0, key = "h_op_fa")
        inletfa = grid3.selectbox('Air inlet',air_inlets, key = "inletfa")
        rollerfa = grid3.selectbox('Roller shutter box',roller_shutter_boxes, key = "rollerfa")
    
    else:
        st.write('Reception room')
        grid1 = grid([2,3,3],[2,3,3],[2,3,3],[2,3,3],vertical_align="bottom")
        grid1.checkbox("Separative wall")
        material1 = grid1.selectbox('Separative',materials, key = "material1")
        linings1 = grid1.selectbox('Doubling',linings, key="linings1")
        grid1.checkbox("Room walls")
        materialw1 = grid1.selectbox('Material',materials, key = "materialw1")
        liningw1 = grid1.selectbox('Doubling',linings, key = "liningw1")
        grid1.checkbox("Room facade")
        materialfa = grid1.selectbox('Material',materials, key = "materialfa")
        liningfa1 = grid1.selectbox('Doubling',linings, key = "liningfa1")
        grid1.checkbox("Room floor")
        materialf1 = grid1.selectbox('Material',materials,0, key = "materialf1")
        liningf1 = grid1.selectbox('Screed',linings, key = "liningf1")
        grid1.checkbox("Room ceiling")
        materialc1 = grid1.selectbox('Material',materials, key = "materialc1")
        liningc1 = grid1.selectbox('Doubling',linings, key = "liningc1")
        st.markdown("<hr style='border: 1px solid grey;'/>", unsafe_allow_html=True)

    
        if room_choice == "Adjacent":
            st.write('Adjacent')
            grid2 = grid([2,3,3],[2,3,3],[2,3,3],[2,3,3],[2,3,3],vertical_align="bottom")
            grid2.checkbox("Room2 - adjacent")
            grid2.write(material1)
            linings2 = grid2.selectbox('Doubling',linings, key="linings2")
            grid2.checkbox("Room2 walls")
            grid2.write(materialw1)
            liningw2 = grid2.selectbox('Doubling',linings, key="liningw2")
            grid2.checkbox("Room2 facade")
            grid2.write(materialfa)
            liningfa2 = grid2.selectbox('Doubling',linings, key = "liningfa2")
            grid2.checkbox("Room2 floor")
            grid2.write(materialf1)
            liningf2 = grid2.selectbox('Doubling',linings, key="liningf2")
            grid2.checkbox("Room2 ceiling")
            grid2.write(materialc1)
            liningc2 = grid2.selectbox('Doubling',linings, key="liningc2")
            st.markdown("<hr style='border: 1px solid grey;'/>", unsafe_allow_html=True)
       
    # if room_choice == "Up":
    #     st.write('Up')
    #     grid2 = grid([2,2,2,2],[2,3,3],[2,3,3],[2,3,3],vertical_align="bottom")
    #     grid2.checkbox("Room2 - Room")
    #     grid2.selectbox('Separative',materials, key = "material02")
    #     grid2.selectbox('Doubling',linings, key="linings02")
    #     grid2.selectbox('Openings',openings, key="opening02")
    #     grid2.checkbox("Walls")
    #     grid2.selectbox('Separative',materials, key = "material12")
    #     grid2.selectbox('Doubling',linings, key="linings12")
    #     grid2.checkbox("Floor")
    #     grid2.selectbox('Separative',materials, key = "material22")
    #     grid2.selectbox('Doubling',linings, key="linings22")
    #     grid2.checkbox("Ceiling")
    #     grid2.selectbox('Separative',materials, key = "material32")
    #     grid2.selectbox('Doubling',linings, key="linings32")
    #     st.markdown("<hr style='border: 1px solid grey;'/>", unsafe_allow_html=True)
            
    # if room_choice == "Down":
    #     st.write('Down')
    #     grid2 = grid([2,2,2,2],[2,3,3],[2,3,3],[2,3,3],vertical_align="bottom")
    #     grid2.checkbox("Room2 - Room")
    #     grid2.selectbox('Separative',materials, key = "material02")
    #     grid2.selectbox('Doubling',linings, key="linings02")
    #     grid2.selectbox('Openings',openings, key="opening02")
    #     grid2.checkbox("Walls")
    #     grid2.selectbox('Separative',materials, key = "material12")
    #     grid2.selectbox('Doubling',linings, key="linings12")
    #     grid2.checkbox("Floor")
    #     grid2.selectbox('Separative',materials, key = "material22")
    #     grid2.selectbox('Doubling',linings, key="linings22")
    #     grid2.checkbox("Ceiling")
    #     grid2.selectbox('Separative',materials, key = "material32")
    #     grid2.selectbox('Doubling',linings, key="linings32")
    #     st.markdown("<hr style='border: 1px solid grey;'/>", unsafe_allow_html=True)
        
    if st.button("Calculation"):
        
        if room_choice == "Adjacent":
        
            st.session_state.numeric_values = []
             # Get selected materials
            selected_material1 = st.session_state.material1
            selected_linings1 = st.session_state.linings1
            selected_openings = st.session_state.openings
            selected_materialw1 = st.session_state.materialw1
            selected_liningw1 = st.session_state.liningw1
            selected_materialf1 = st.session_state.materialf1
            selected_liningf1 = st.session_state.liningf1
            selected_materialc1 = st.session_state.materialc1
            selected_liningc1 = st.session_state.liningc1
            selected_linings2 = st.session_state.linings2
            selected_liningw2 = st.session_state.liningw2
            selected_liningf2 = st.session_state.liningf2
            selected_liningc2 = st.session_state.liningc2
            selected_materialfa = st.session_state.materialfa
            selected_liningfa1 = st.session_state.liningfa1
            selected_liningfa2 = st.session_state.liningfa2
            selected_l =  st.session_state.l
            selected_L =  st.session_state.L
            selected_h =  st.session_state.h     
            selected_L2 = st.session_state.L2

           
            # Convert to strings
            material1_str = str(selected_material1)
            linings1_str = str(selected_linings1)
            openings_str = str(selected_openings)
            materialw1_str = str(selected_materialw1)
            liningw1_str = str(selected_liningw1)
            materialf1_str = str(selected_materialf1)
            liningf1_str = str(selected_liningf1)
            materialc1_str = str(selected_materialc1)
            liningc1_str = str(selected_liningc1)
            linings2_str = str(selected_linings2)
            liningw2_str = str(selected_liningw2)
            liningf2_str = str(selected_liningf2)
            liningc2_str = str(selected_liningc2)
            materialfa_str = str(selected_materialfa)
            liningfa1_str = str(selected_liningfa1)
            liningfa2_str = str(selected_liningfa2)
            l_str = (str(selected_l))
            L_str = (str(selected_L))
            h_str = (str(selected_h))
            L2_str = (str(selected_L2))
            
            result = subprocess.run(["python", "DnT_calculation.py", material1_str,linings1_str,openings_str,materialw1_str,liningw1_str,materialf1_str,liningf1_str,materialc1_str,liningc1_str,linings2_str,liningw2_str,liningf2_str,liningc2_str,l_str,L_str,h_str,L2_str], capture_output=True, text=True)
            st.text("Result:")
            st.text(result.stdout)
            stdout_output_str = str(result.stdout)
                  
            # Split the string into words
            clean = stdout_output_str.replace(',','')
            clean = clean.replace('[','')
            clean = clean.replace(']','')
            results = clean.split()
            results = [float(num) if num.replace('.', '', 1).isdigit() or (num.startswith('-') and num[1:].replace('.', '', 1).isdigit()) else num for num in results]
    
            for i in range(4,25):
                st.session_state.numeric_values.append(results[i])
            fig_result, ax_result = plt.subplots()
            ax_result.set_xscale('log')
            ax_result.set_xticks(freq)
            ax_result.get_xaxis().set_major_formatter(plt.ScalarFormatter())
            ax_result.get_xaxis().set_tick_params(which='minor', size=0)
            ax_result.get_xaxis().set_tick_params(which='minor', width=0) 
            ax_result.tick_params(axis='x', rotation=90)
            ax_result.plot(freq, results[4:25], label = "DnT")
            ax_result.plot(freq, results[28:49], label = "DnT_direct")
            ax_result.plot(freq, results[52:73], label = "DnT_walls")
            ax_result.plot(freq, results[76:97], label = "DnT_floor")
            ax_result.plot(freq, results[100:121], label = "DnT_ceiling")
            ax_result.set_xlabel('Frequency (Hz)')
            ax_result.set_ylabel('Airborne sound insulation (dB)')
            ax_result.set_title('Calculation result')
            ax_result.legend()
            ax_result.grid(which = "major")
            st.pyplot(fig_result)

        
        if room_choice == "Exterior":

            st.session_state.numeric_values = []
             # Get selected materials
            selected_materialfa = st.session_state.materialfa
            selected_liningfa1 = st.session_state.liningfa1
            selected_openingfa = st.session_state.openingfa  
            selected_inletfa = st.session_state.inletfa
            selected_rollerfa = st.session_state.rollerfa
            selected_l_op_fa = st.session_state.l_op_fa
            selected_h_op_fa = st.session_state.h_op_fa
            selected_l =  st.session_state.l
            selected_L =  st.session_state.L
            selected_h =  st.session_state.h 
            
            # Convert to strings
            materialfa_str = str(selected_materialfa)
            liningfa1_str = str(selected_liningfa1)
            openingfa_str = str(selected_openingfa)
            inletfa_str = str(selected_inletfa)
            rollerfa_str = str(selected_rollerfa)
            l_op_fa_str = str(selected_l_op_fa)
            h_op_fa_str = str(selected_h_op_fa)
            l_str = (str(selected_l))
            L_str = (str(selected_L))
            h_str = (str(selected_h))   
            
            result = subprocess.run(["python", "DnT_calculation_facade.py", materialfa_str, liningfa1_str, openingfa_str, inletfa_str, rollerfa_str, l_op_fa_str, h_op_fa_str,l_str, L_str, h_str], capture_output=True, text=True)
            st.text("Result:")
            st.text(result.stdout)
            stdout_output_str = str(result.stdout)

            # Split the string into words
            clean = stdout_output_str.replace(',','')
            clean = clean.replace('[','')
            clean = clean.replace(']','')
            results = clean.split()
            results = [float(num) if num.replace('.', '', 1).isdigit() or (num.startswith('-') and num[1:].replace('.', '', 1).isdigit()) else num for num in results]
    
            for i in range(4,25):
                st.session_state.numeric_values.append(results[i])
            fig_result, ax_result = plt.subplots()
            ax_result.set_xscale('log')
            ax_result.set_xticks(freq)
            ax_result.get_xaxis().set_major_formatter(plt.ScalarFormatter())
            ax_result.get_xaxis().set_tick_params(which='minor', size=0)
            ax_result.get_xaxis().set_tick_params(which='minor', width=0) 
            ax_result.tick_params(axis='x', rotation=90)
            ax_result.plot(freq, results[4:25], label = "D_2m_nT")
            ax_result.set_xlabel('Frequency (Hz)')
            ax_result.set_ylabel('Facade sound insulation (dB)')
            ax_result.set_title('Calculation result')
            ax_result.legend()
            ax_result.grid(which = "major")
            st.pyplot(fig_result)     
                
 
    title = st.text_input('Calculation name', value="")
    if st.button("save"):
        list_name = title
        st.session_state.user_dnt[list_name] = st.session_state.numeric_values
        st.text('saved');
        # st.write(list_name)
        # st.write("resulting list:", session_state.user_dnt[list_name])
        
