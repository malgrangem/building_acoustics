# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 09:25:10 2022

@author: M3309200
"""

import xlrd
import numpy as np
from acoustics.weighting import *
from acoustics.decibel import *
from acoustics.bands import *

class Room:
    def __init__(self, l, L, h):
        self.l = l
        self.L = L
        self.h = h
    
    def calc_area(self):
        self.area = self.l * self.L
        return self.area
    
    def calc_volume(self):
        self.volume = self.calc_area() * self.h
        return self.volume
    
    def wall_properties(self):
        pass
    
    def vert(self):
        return [self.L,self.h]
    
    def hor(self):
        return[self.L,self.l]
    
    def sep(self):
        return[self.l,self.h]
            
class Material:
    def __init__(self, name, thickness, cat, ms, sri, ts, aeq):
        self.name = name
        self.thickness = thickness
        self.cat = cat
        self.ms = ms
        self.sri = sri
        self.ts = ts
        self.aeq = aeq


    def structural_time(self):
        self.ts = []
        self.aeq = []
        for i in freq:
            if self.cat == 1:
                self.ts.append(2.2/(i*(np.power(10,(-12-3.3*np.log10(i/100))/10)))) #formule empirique pour Ts in situ
                #self.ts.append(2.2/(i*(0.011*(1+0.25*(self.ms/np.power(i,0.5)))))) #formule 12354 Ts labo
            
            if self.cat == 2:
                self.ts.append(2.01*np.power(i,-0.5))
              
        return self.ts
    
    
    def eq_abs_length(self):
        self.a_eq = []
        for idx, i in enumerate(freq):
            self.a_eq.append(2.2*np.power(np.pi,2)*np.power(1000/i,0.5)/(340*self.ts[idx]))
        return self.a_eq
        
       
class Opening(Material):
    def __init__(self,l,h,sri):
        self.l = l
        self.h = h
        self.sri = sri
        
    def calc_area(self):
        self.area = self.l * self.h
        return self.area

class Lining(Material):
    def __init__(self,name,thickness,d_sri):
        self.name = name
        self.thickness = thickness
        self.d_sri = d_sri
        
class Element():
    def __init__(self,n_sri):
        self.n_sri = n.sri


class Air_inlet(Element):
    def __init__(self,n_sri):
        self.n_sri = n_sri
        
class Roller_shutter_box(Element):
    def __init__(self,n_sri):
        self.n_sri = n_sri

class Source:
    def __init__(self,name,lvl,lvla):
        self.name = name
        self.lvl = lvl
        self.lvla = lvla

## A_weighting octave function

OCTAVE_A_WEIGHTING = np.array([-56.7, -39.4, -26.2, -16.1, -8.6, -3.2, +0.0, +1.2, +1.0, -1.1, -6.6]) 

def a_weighting_oct(first,last):
    oct_bands = octave(16,16000)
    low_index = np.where(oct_bands == first)[0]
    high_index = np.where(oct_bands == last)[0]

    if len(low_index) == 0 or len(high_index) == 0:
        raise ValueError("One or both of the specified frequencies not found in octave bands.")

    low = low_index[0]
    high = high_index[0]
    
    freq_weightings = OCTAVE_A_WEIGHTING

    return freq_weightings[low: high+1]
        
def z2a_oct(levels, first, last):
    """Apply A-weighting to Z-weighted signal, in octave bands.
    """
    return levels + a_weighting_oct(first, last)


####Lecture du fichier de données des éléments de construction####

materials = []
openings = []
linings = []
air_inlets = []
roller_shutter_boxes = []
sri = []
d_sri = []
n_sri = []
freq = []
sources = []
nr = []




df = xlrd.open_workbook('database.xls')
noise_database = xlrd.open_workbook('noise_database.xls')

#freq
for i in range(4,25):
    freq.append(int(df.sheet_by_name('Materials').cell_value(i,0)))

#Materials
for i in range(1,df.sheet_by_name('Materials').ncols):
    materials.append(df.sheet_by_name('Materials').cell_value(0,i))
    sri = []
    ts = []
    aeq = []
    
    for j in range(21):
        sri.append(df.sheet_by_name('Materials').cell_value(j+4,i))
     
        if df.sheet_by_name('Materials').cell_value(2,i) == 1:
            ts.append(2.2/(freq[j]*np.power(10,-12-3.3*np.log10(freq[j]/100))))
            aeq.append(2.2*np.pi*np.pi*(np.power((1000/freq[j]),0.5))/(340*(2.2/(freq[j]*np.power(10,(-12-3.3*np.log10(freq[j]/100))/10)))))
        else:
            ts.append(2.01*np.power(freq[j],-0.5))
            aeq.append(2.2*np.pi*np.pi*(np.power((1000/freq[j]),0.5))/(340*(2.01*np.power(freq[j],-0.5))))

        
    globals()[df.sheet_by_name('Materials').cell_value(0,i)] = Material(df.sheet_by_name('Materials').cell_value(0,i),df.sheet_by_name('Materials').cell_value(1,i),int(df.sheet_by_name('Materials').cell_value(2,i)),df.sheet_by_name('Materials').cell_value(3,i), sri, ts, aeq)
    

#Openings
for i in range(1,df.sheet_by_name('Openings').ncols):
    openings.append(df.sheet_by_name('Openings').cell_value(0,i))
    sri = [] 
    for j in range(3,df.sheet_by_name('Openings').nrows):
        sri.append(df.sheet_by_name('Openings').cell_value(j,i))
        globals()[df.sheet_by_name('Openings').cell_value(0,i)] = Opening(df.sheet_by_name('Openings').cell_value(1,i),df.sheet_by_name('Openings').cell_value(2,i), sri)
 
#Linings
for i in range(1,df.sheet_by_name('Linings').ncols):
    linings.append(df.sheet_by_name('Linings').cell_value(0,i))
    d_sri = [] 
    for j in range(2,df.sheet_by_name('Linings').nrows):
        d_sri.append(df.sheet_by_name('Linings').cell_value(j,i))
    
    globals()[df.sheet_by_name('Linings').cell_value(0,i)] = Lining(df.sheet_by_name('Linings').cell_value(0,i),df.sheet_by_name('Linings').cell_value(1,i), d_sri)
      
#Air_inlets
for i in range(1,df.sheet_by_name('Air_inlets').ncols):
    air_inlets.append(df.sheet_by_name('Air_inlets').cell_value(0,i))
    n_sri = []
    for j in range(1,df.sheet_by_name('Air_inlets').nrows):
        n_sri.append(df.sheet_by_name('Air_inlets').cell_value(j,i))
     
    globals()[df.sheet_by_name('Air_inlets').cell_value(0,i)] = Air_inlet(n_sri)
   
#Roller_shutter_boxes
for i in range(1,df.sheet_by_name('Roller_shutter_boxes').ncols):
    roller_shutter_boxes.append(df.sheet_by_name('Roller_shutter_boxes').cell_value(0,i))
    n_sri = []
    for j in range(1,df.sheet_by_name('Roller_shutter_boxes').nrows):
        n_sri.append(df.sheet_by_name('Roller_shutter_boxes').cell_value(j,i))
     
    globals()[df.sheet_by_name('Roller_shutter_boxes').cell_value(0,i)] = Roller_shutter_box(n_sri)
    
# Sources
for i in range(2,noise_database.sheet_by_name('Data').nrows):
    sources.append(noise_database.sheet_by_name('Data').cell_value(i,0))
    lvl =[]
    
    
    for j in range(2,noise_database.sheet_by_name('Data').ncols):
        lvl.append(noise_database.sheet_by_name('Data').cell_value(i,j))
    lvla = round(dbsum(z2a(lvl, 50, 5000)),1)
    
    globals()[noise_database.sheet_by_name('Data').cell_value(i,0)] = Source(noise_database.sheet_by_name('Data').cell_value(i,0),lvl,lvla)

for i in range(2,noise_database.sheet_by_name('NR').nrows):
    nr.append(noise_database.sheet_by_name('NR').cell_value(i,0))
    lvl =[]
    for j in range(2,noise_database.sheet_by_name('NR').ncols):
        lvl.append(noise_database.sheet_by_name('NR').cell_value(i,j))
    lvla = round(dbsum(z2a_oct(lvl, 63, 4000)),1)
    
    globals()[noise_database.sheet_by_name('NR').cell_value(i,0)] = Source(noise_database.sheet_by_name('NR').cell_value(i,0),lvl,lvla)
    
   
# Facade

D_2m_nT = [] #isolement de facade
tau_wall_facade = [] 
tau_opening_facade = []
tau_air_inlet = [] 
tau_shutter = []
dr_fac_2 = [] #efficacité du doublage facade côté room2
dr_fac_1 = [] #efficacité du doublage facade côté room1     


#Intérieur

tau_wall_separative = [] 
tau_opening_separative = []
DnT_direct = [] #isolement par la paroi séparative
Dn1_df = [] #isolement latéral 1, transmission direct-flanking (séparatif-sol)
Dn1_ff = [] #isolement latéral 1, transmission flanking-flanking (sol-sol)
Dn1_fd = [] #isolement latéral 1, transmission flanking-direct (sol-séparatif)
DnT1 = [] #isolement latéral1 (jonction entre sol et séparatif)
Dn2_df = [] #isolement latéral 2, transmission direct-flanking (séparatif-mur intérieur)
Dn2_ff = [] #isolement latéral 2, transmission flanking-flanking (mur intérieur-mur intérieur)
Dn2_fd = [] #isolement latéral 2, transmission flanking-direct (mur intérieur-séparatif)
DnT2 = [] #isolement latéral2 (jonction entre mur intérieur et séparatif)
Dn3_df = [] #isolement latéral 3, transmission direct-flanking (séparatif-plafond)
Dn3_ff = [] #isolement latéral 3, transmission flanking-flanking (plafond-plafond)
Dn3_fd = [] #isolement latéral 3, transmission flanking-direct (plafond-séparatif)
DnT3 = [] #isolement latéral3 (jonction entre plafond et séparatif)
Dn4_df = [] #isolement latéral 4, transmission direct-flanking (séparatif-facade)
Dn4_ff = [] #isolement latéral 4, transmission flanking-flanking(facade-facade)
Dn4_fd = [] #isolement latéral 4, transmission flanking-direct (facade-séparatif)
DnT4 = [] #isolement latéral4 (jonction entre facade et séparatif)
DnT = [] #isolement global

dr_sep_2 = [] #efficacité du doublage sur séparatif, côté room2
dr_sep_1 = [] #efficacité du doublage sur séparatif, côté room1
dr_wall_2 = [] #efficacité du doublage sur mur intérieur, côté room2 
dr_wall_1 = [] #efficacité du doublage sur mur intérieur, côté room1 
dr_ceil_2 = [] #efficacité du faux-plafond, côté room2
dr_ceil_1 = [] #efficacité du faux-plafond, côté room1 
dr_floor_2 = [] #efficacité de la chape, côté room2
dr_floor_1 = []  #efficacité de la chape côté room1  
    
msg = 0 #variable de vérification de la correspondance doublage/mur support    