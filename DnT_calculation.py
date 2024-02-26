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

material1 = sys.argv[1]
linings1 = sys.argv[2]
openings = sys.argv[3]
materialw1 = sys.argv[4]
liningw1 = sys.argv[5]
materialf1 = sys.argv[6]
liningf1 = sys.argv[7]
materialc1 = sys.argv[8]
liningc1 = sys.argv[9]
linings2 = sys.argv[10]
liningw2 = sys.argv[11]
liningf2 = sys.argv[12]
liningc2 = sys.argv[13]
l = float(sys.argv[14])
L1 = float(sys.argv[15])
h = float(sys.argv[16])
L2 = float(sys.argv[17])

# from SGSF_acoustic_tool.py import material1
# linings1, openings, materialw1, liningw1, materialf1, liningf1, materialc1, liningc1, linings2, liningw2, liningf2, liningc2


# def main(material1, linings1, openings, materialw1, liningw1, materialf1, liningf1, materialc1, liningc1, linings2, liningw2, liningf2, liningc2):
#     # Your existing code here



######### GLOBAL PARAMETERS

case = 2 # 1 = facade calculation / 2 = room calculation

# l = eval(l)
# L1 = 3
# L2 = 3
# h = 2.5

room1 = Room(l,L1,h) #reception room
room2 = Room(l,L2,h) #emission room

#Facade materials definition
wall_facade = eval(materialw1)
lining_facade_em = eval(liningw2)
lining_facade_rec = eval(liningw1)
# opening_facade = None
# air_inlet = None
# roller_shutter_box = None

# #Other materials
floor = eval(materialf1)
ceiling = eval(materialc1)
separative = eval(material1)
opening_sep = eval(openings)
lining_sep_em = eval(linings2)
lining_sep_rec = eval(linings1)
lining_wall_em = eval(liningw2)
lining_wall_rec = eval(liningw1)
lining_ceil_em = eval(liningc2)
lining_ceil_rec = eval(liningc1)
lining_floor_em = eval(liningf2)
lining_floor_rec = eval(liningf1)
wall_int = eval(materialw1)


#Calculation inputs 

s_floor_em = L2*l
s_floor_rec =L1*l
s_int_em = L2*h
s_int_rec = L1*h
s_sep = l*h
s_opening = 0

c = 10*np.log10(0.032*room1.calc_volume())

######## FACADE CALCULATION

# if case == 1:

#     #Direct transmission calculation
    
#     if lining_facade_em != None and (wall_facade.name in lining_facade_em.name) is True:
#         dr_fac_em = lining_facade_em.d_sri
#     elif lining_facade_em == None :
#         dr_fac_em = [0]*21
#     else: 
#         msg = 1
        
#     if lining_facade_rec != None and (wall_facade.name in lining_facade_rec.name) is True:
#         dr_fac_rec = lining_facade_rec.d_sri
#     elif lining_facade_rec == None :
#         dr_fac_rec = [0]*21
#     else: 
#         msg = 1
    
#     for i in range(len(freq)): 
    
#         if opening_facade is None:
#             tau_opening_facade = [0]*21
#             tau_wall_facade.append((h*L1/10)*np.power(10,(-wall_facade.sri[i]-dr_fac_rec[i])/10)) #Facade wall without window
#         else:
#             tau_opening_facade.append((opening_facade.h*opening_facade.l/10)*(np.power(10,-opening_facade.sri[i]/10))) #Opening
#             tau_wall_facade.append((((h*L1)-(opening_facade.h*opening_facade.l))/10)*np.power(10,-wall_facade.sri[i]/10))#Facade wall 
        
#         if air_inlet is None:
#             tau_air_inlet = [0]*21
#         else:
#             tau_air_inlet.append(np.power(10,-air_inlet.n_sri[i]/10))
            
#         if roller_shutter_box is None:
#             tau_shutter = [0]*21
#         else: tau_shutter.append((opening_facade.l/1.4)*np.power(10,-roller_shutter_box.n_sri[i]/10))
        
#         D_2m_nT.append(-10*np.log10(tau_wall_facade[i]+tau_opening_facade[i]+tau_air_inlet[i]+tau_shutter[i]) + 10*np.log10(0.032*l*L1*h))
    
    
#     # Tracé du spectre
#     fig, ax = plt.subplots(figsize=(6,10))
#     ax.plot(freq, D_2m_nT)
#     ax.set_xscale("log") 
#     ax.set_xticks(freq)
#     ax.set_xticklabels(freq, rotation=45)
#     ax.set_ylim(ymin=0)
#     ax.set_title("D_2m_nT")
#     ax.grid()
    
#     resultf = building.rw(D_2m_nT[3:19])
#     resultfc = resultf - building.rw_c(D_2m_nT[3:19])
#     resultfctr = resultf - building.rw_ctr(D_2m_nT[3:19])
    
#     print ('D2m,nT,w (C;Ctr) = %d(-%d;-%d)' % (resultf,resultfc,resultfctr))

######## INSULATION BETWEEN ROOMS

if case == 2:

    #Junction calculations
    
        def junction(mat1, mat2, t): #t = type de jonction, homogène, mixte, légère ou cas particulier pour séparative en double ossature
            
            M = np.log10(mat2.ms/mat1.ms)
            Mbis = np.log10(mat1.ms/mat2.ms)
            K11 = []
            K12 = []
            #K22 = []
            
            for i in freq: 
                if t == 'h':
                    K11.append(6.7+14.1*M+5.7*np.power(M,2))
                    K12.append(6.7+5.7*np.power(M,2))
                    #K22 = [0]*21
           
                if t == 'm':
                    # K11.append(7.5+20*np.power(M,2)-3.3*np.log10(i/500))
                    K11.append(4.7-14.1*M+5.7*np.power(M,2))
                    K12.append(7.5+10*np.power(M,2)+3.3*np.log10(i/500))
                    #K22.append(4.7-14.1*M+5.7*np.power(M,2)) 
                
                if t == 'l':
                    K11.append(max(10,10+20*(Mbis)-3.3*np.log10(i/500)))
                    K12.append(10+10*np.abs(Mbis)-3.3*np.log10(i/500))
                    #K22.append(max(10,10-20*M-3.3*np.log10(i/500)))
                
                if t == 'd':
                    K11.append(20+max(10,10+20*(Mbis)-3.3*np.log10(i/500)))
                    K12.append(30+10*np.abs(Mbis)-3.3*np.log10(i/500))                    
            
            return M, K11, K12  
              
        def Dvij(mat1,mat2,t,lj,l,h,L1,L2): 
            
            dv11 = []
            dv12 = []
            dv21 = []
            #dv22 = []
        
           
            for idx, i in enumerate(freq):
                dv11.append(max(0,junction(mat1,mat2,t)[1][idx]-10*np.log10(lj/np.power(lj*L2*mat2.aeq[idx]*lj*L1*mat2.aeq[idx],0.5))))
                dv12.append(max(0,junction(mat1,mat2,t)[2][idx]-10*np.log10(lj/np.power(lj*L2*mat2.aeq[idx]*h*l*mat1.aeq[idx],0.5))))
                dv21.append(max(0,junction(mat1,mat2,t)[2][idx]-10*np.log10(lj/np.power(lj*L1*mat1.aeq[idx]*h*l*mat2.aeq[idx],0.5))))
                #dv22.append(max(0,junction(mat1,mat2)[3][idx]-10*np.log10(l/np.power(s1*mat1.eq_abs_length()[idx]*s2*mat2.eq_abs_length()[idx],0.5))))
            
            return dv11, dv12, dv21
            
        if lining_sep_em != None and (separative.name in lining_sep_em.name) is True:
            dr_sep_em = lining_sep_em.d_sri
        elif lining_sep_em == None:
            dr_sep_em = [0]*21
        else:
            msg = 1
            
        if lining_sep_rec != None and (separative.name in lining_sep_rec.name) is True:
            dr_sep_rec = lining_sep_rec.d_sri
        elif lining_sep_rec == None:
            dr_sep_rec = [0]*21
        else: 
            msg = 1
        
        if lining_wall_em != None and (wall_int.name in lining_wall_em.name) is True:
            dr_wall_em = lining_wall_em.d_sri
        elif lining_wall_em == None:
            dr_wall_em = [0]*21
        else: 
            msg = 1
        
        if lining_wall_rec != None and (wall_int.name in lining_wall_rec.name) is True:
            dr_wall_rec = lining_wall_rec.d_sri
        elif lining_wall_rec == None:
            dr_wall_rec = [0]*21
        else: 
            msg = 1
            
        if lining_facade_em != None and (wall_facade.name in lining_facade_em.name) is True:
            dr_fac_em = lining_facade_em.d_sri
        elif lining_facade_em == None :
            dr_fac_em = [0]*21
        else: 
            msg = 1
        
        if lining_facade_rec != None and (wall_facade.name in lining_facade_rec.name) is True:
            dr_fac_rec = lining_facade_rec.d_sri
        elif lining_facade_rec == None :
            dr_fac_rec = [0]*21
        else: 
            msg = 1    
        
        if lining_floor_em != None:
            dr_floor_em = lining_floor_em.d_sri
        else: 
            dr_floor_em = [0]*21
        
        if lining_floor_rec != None:
            dr_floor_rec = lining_floor_rec.d_sri
        else: 
            dr_floor_rec = [0]*21
        
        if lining_ceil_em != None:
            dr_ceil_em = lining_ceil_em.d_sri
        else: 
            dr_ceil_em = [0]*21
        
        if lining_ceil_rec != None:
            dr_ceil_rec = lining_ceil_rec.d_sri
        else: 
            dr_ceil_rec = [0]*21
        
    
        
        #direct
        
        for i in range(len(freq)):
            
            if msg == 1:
                print("Erreur de définition doublage, calcul stoppé")
                break
            else:
            
                DnT_direct.append(round(separative.sri[i] + dr_sep_em[i] + dr_sep_rec[i] - 10*np.log10(l*h/10) + 10*np.log10(0.032*room1.calc_volume()),1))
            
            #lateral1 ; floor
                
                if separative.cat == 1:
                    t = 'h'
                if (separative.cat == 2 or separative.cat == 3) :
                    t = 'm'
            
                Dn1_df.append(Dvij(separative,floor,t,l,l,h,L1,L2)[2][i]+(dr_sep_em[i] + separative.sri[i]/2 + dr_floor_rec[i] + floor.sri[i]/2)-10*np.log10((np.power(s_floor_rec*s_sep,0.5))/10)+10*np.log10(0.032*room1.calc_volume()))
                Dn1_ff.append(Dvij(separative,floor,t,l,l,h,L1,L2)[0][i]+(dr_floor_em[i] + floor.sri[i]/2+ dr_floor_rec[i] + floor.sri[i]/2)-10*np.log10((np.power(s_floor_em*s_floor_rec,0.5))/10)+10*np.log10(0.032*room1.calc_volume()))
                Dn1_fd.append(Dvij(separative,floor,t,l,l,h,L1,L2)[1][i]+(dr_floor_em[i] + floor.sri[i]/2 + dr_sep_rec[i] + separative.sri[i]/2)-10*np.log10((np.power(s_floor_em*s_sep,0.5))/10)+10*np.log10(0.032*room1.calc_volume()))
            
                DnT1.append(round(-10*np.log10(np.power(10,-Dn1_df[i]/10)+np.power(10,-Dn1_ff[i]/10)+np.power(10,-Dn1_fd[i]/10)),1))
                
            #lateral2 ; wall_int
                
                if separative.cat == 2 and ((wall_int.cat == 2) or (wall_int.cat == 3)):
                    t = 'l'
                if separative.cat == 3 and ((wall_int.cat == 2) or (wall_int.cat == 3)):
                    t = 'd'
                    # print(t)
                if separative.cat == 2 and wall_int.cat == 1:
                    t = 'm'
                if separative.cat == 1 and wall_int.cat == 1:
                    t = 'h'
             
                Dn2_df.append(Dvij(separative,wall_int,t,h,l,h,L1,L2)[2][i]+(dr_sep_em[i] + separative.sri[i]/2 + dr_wall_rec[i] + wall_int.sri[i]/2)-10*np.log10((np.power(s_sep*s_int_rec,0.5))/10)+10*np.log10(0.032*room1.calc_volume()))
                Dn2_ff.append(Dvij(separative,wall_int,t,h,l,h,L1,L2)[0][i]+(dr_wall_em[i] + wall_int.sri[i]/2 + dr_wall_rec[i] + wall_int.sri[i]/2)-10*np.log10((np.power(s_int_em*s_int_rec,0.5))/10)+10*np.log10(0.032*room1.calc_volume()))
                Dn2_fd.append(Dvij(separative,wall_int,t,h,l,h,L1,L2)[1][i]+(dr_wall_em[i] + wall_int.sri[i]/2 + dr_sep_rec[i] + separative.sri[i]/2)-10*np.log10((np.power(s_int_em*s_sep,0.5))/10)+10*np.log10(0.032*room1.calc_volume())) 
            
                DnT2.append(round(-10*np.log10(np.power(10,-Dn2_df[i]/10)+np.power(10,-Dn2_ff[i]/10)+np.power(10,-Dn2_fd[i]/10)),1))
            
            #lateral3 ; ceiling
                
                if separative.cat == 1:
                    t = 'h'
                if (separative.cat == 2 or separative.cat == 3):
                    t = 'm'
            
                Dn3_df.append(Dvij(separative,floor,t,l,l,h,L1,L2)[2][i]+(dr_sep_em[i] + separative.sri[i]/2 + dr_ceil_rec[i] + floor.sri[i]/2)-10*np.log10((np.power(s_floor_rec*s_sep,0.5))/10)+10*np.log10(0.032*room1.calc_volume()))
                Dn3_ff.append(Dvij(separative,floor,t,l,l,h,L1,L2)[0][i]+(dr_ceil_em[i] + floor.sri[i]/2 + dr_ceil_rec[i] + floor.sri[i]/2)-10*np.log10((np.power(s_floor_em*s_floor_rec,0.5))/10)+10*np.log10(0.032*room1.calc_volume()))
                Dn3_fd.append(Dvij(separative,floor,t,l,l,h,L1,L2)[1][i]+(dr_ceil_em[i] + floor.sri[i]/2 + dr_sep_rec[i] + separative.sri[i]/2)-10*np.log10((np.power(s_floor_em*s_sep,0.5))/10)+10*np.log10(0.032*room1.calc_volume()))
            
                DnT3.append(round(-10*np.log10(np.power(10,-Dn3_df[i]/10)+np.power(10,-Dn3_ff[i]/10)+np.power(10,-Dn3_fd[i]/10)),1))
                
            #lateral4 ; wall_facade
            
                if separative.cat == 1:
                    t = 'h'
                if (separative.cat == 2 or separative.cat == 3):
                    t = 'm'
             
               
                Dn4_df.append(Dvij(separative,wall_facade,t,h,l,h,L1,L2)[2][i]+(dr_sep_em[i] + separative.sri[i]/2 + dr_fac_rec[i] + wall_facade.sri[i]/2)-10*np.log10((np.power(s_int_rec*s_sep,0.5))/10)+10*np.log10(0.032*room1.calc_volume()))
                Dn4_ff.append(Dvij(separative,wall_facade,t,h,l,h,L1,L2)[0][i]+(dr_fac_em[i] + wall_facade.sri[i]/2 + dr_fac_rec[i] + wall_facade.sri[i]/2)-10*np.log10((np.power(s_int_rec*s_int_em,0.5))/10)+10*np.log10(0.032*room1.calc_volume()))
                Dn4_fd.append(Dvij(separative,wall_facade,t,h,l,h,L1,L2)[1][i]+(dr_fac_em[i] + wall_facade.sri[i]/2 + dr_sep_rec[i] + separative.sri[i]/2)-10*np.log10((np.power(s_int_em*s_sep,0.5))/10)+10*np.log10(0.032*room1.calc_volume())) 
            
                DnT4.append(round(-10*np.log10(np.power(10,-Dn4_df[i]/10)+np.power(10,-Dn4_ff[i]/10)+np.power(10,-Dn4_fd[i]/10)),1))
                
            #Global
            
                DnT.append(round(-10*np.log10(np.power(10,-DnT_direct[i]/10)+np.power(10,-DnT1[i]/10)+np.power(10,-DnT2[i]/10)+np.power(10,-DnT3[i]/10)+np.power(10,-DnT4[i]/10)),1))
        
        
        # Tracé du spectre
        fig, ax = plt.subplots(figsize=(6,10))
        ax.plot(freq, DnT)
        ax.set_xscale("log") 
        ax.set_xticks(freq)
        ax.set_xticklabels(freq, rotation=45)
        ax.set_ylim(ymin=0)
        ax.set_title('DnT')
        ax.grid()
        
        if len(DnT) == 21:
            resultr = building.rw(DnT[3:19])
            resultrc = resultr - building.rw_c(DnT[3:19])
            resultrctr = resultr - building.rw_ctr(DnT[3:19])
            dnt_direct = building.rw(DnT_direct[3:19])
            dnt_walls = building.rw(DnT4[3:19])
            dnt_floor = building.rw(DnT1[3:19])
            dnt_ceiling = building.rw(DnT3[3:19])
            
            print ('DnT,w (C;Ctr) = %d(-%d;-%d)' % (resultr,resultrc,resultrctr))
            print (DnT)
            print ('DnT_direct = %d' % (dnt_direct))
            print (DnT_direct)
            print ('DnT_walls = %d' % (dnt_walls))
            print (DnT4)
            print ('DnT_floor = %d' % (dnt_floor))
            print (DnT1)
            print ('DnT_ceiling = %d' % (dnt_ceiling))
            print (DnT3)
            
            plt.plot(DnT)

        #DnT writing in excel file
        
        # workbook = xlsxwriter.Workbook('results.xlsx')
        # worksheet = workbook.add_worksheet("4py")
        
        # row = 0
        # column = 0
        
        # worksheet.write(row,1,'DnT_facade_R1')
        # worksheet.write(column,2,'DnT_R2_R1')
        
        # for i in range(len(freq)):
        #     worksheet.write(row+1,column,freq[i])
        #     worksheet.write(row+1,column+1,D_2m_nT[i])
        #     worksheet.write(row+1,column+2,DnT[i])
        #     row+=1
        
        # workbook.close()
