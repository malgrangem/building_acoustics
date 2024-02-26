# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 09:50:34 2022

@author: M3309200
"""

from acoustic_data import*
from initial_data import*
import numpy as np
import matplotlib.pyplot as plt
from acoustics import building
import xlsxwriter
import sys
import io
import base64

materialfa = sys.argv[1]
liningfa1 = sys.argv[2]
openingfa = sys.argv[3]
inletfa = sys.argv[4]
rollerfa = sys.argv[5]
l_op_fa = float(sys.argv[6])
h_op_fa = float(sys.argv[7])
l = float(sys.argv[8])
L1 = float(sys.argv[9])
h = float(sys.argv[10])

######### GLOBAL PARAMETERS

case = 1 # 1 = facade calculation / 2 = room calculation

room1 = Room(l,L1,h) #reception room
room2 = Room(l,L2,h) #emission room

#Facade materials definition
wall_facade = eval(materialfa)
# lining_facade_em = eval(liningfa2)
lining_facade_rec = eval(liningfa1)
opening_facade = eval(openingfa)
air_inlet = eval(inletfa)
roller_shutter_box = eval(rollerfa)

c = 10*np.log10(0.032*room1.calc_volume())

######## FACADE CALCULATION

if case == 1:

    #Direct transmission calculation
    
    # if lining_facade_em != None and (wall_facade.name in lining_facade_em.name) is True:
    #     dr_fac_em = lining_facade_em.d_sri
    # elif lining_facade_em == None :
    #     dr_fac_em = [0]*21
    # else: 
    #     msg = 1
        
    if lining_facade_rec != None and (wall_facade.name in lining_facade_rec.name) is True:
        dr_fac_rec = lining_facade_rec.d_sri
    elif lining_facade_rec == None :
        dr_fac_rec = [0]*21
    else: 
        msg = 1
    
    for i in range(len(freq)): 
    
        if opening_facade is None:
            tau_opening_facade = [0]*21
            tau_wall_facade.append((h*L1/10)*np.power(10,(-wall_facade.sri[i]-dr_fac_rec[i])/10)) #Facade wall without window
        else:
            tau_opening_facade.append((h_op_fa*l_op_fa/10)*(np.power(10,-opening_facade.sri[i]/10))) #Opening
            tau_wall_facade.append((((h*L1)-(h_op_fa*l_op_fa))/10)*np.power(10,-wall_facade.sri[i]/10))#Facade wall 
        
        if air_inlet is None:
            tau_air_inlet = [0]*21
        else:
            tau_air_inlet.append(np.power(10,-air_inlet.n_sri[i]/10))
            
        if roller_shutter_box is None:
            tau_shutter = [0]*21
        else: tau_shutter.append((l_op_fa/1.4)*np.power(10,-roller_shutter_box.n_sri[i]/10))
        
        D_2m_nT.append(round(-10*np.log10(tau_wall_facade[i]+tau_opening_facade[i]+tau_air_inlet[i]+tau_shutter[i]) + 10*np.log10(0.032*l*L1*h),1))
    
    resultf = building.rw(D_2m_nT[3:19])
    resultfc = resultf - building.rw_c(D_2m_nT[3:19])
    resultfctr = resultf - building.rw_ctr(D_2m_nT[3:19])
    
    print ('D2m,nT,w (C;Ctr) = %d(-%d;-%d)' % (resultf,resultfc,resultfctr))
    print(D_2m_nT)

       
        # workbook.close()
