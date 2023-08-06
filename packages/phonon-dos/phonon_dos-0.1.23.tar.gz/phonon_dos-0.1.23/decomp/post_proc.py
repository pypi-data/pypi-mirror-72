#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 14:40:14 2020

@author: gc4217
"""

import numpy as np
from scipy import signal
import os, sys
from decomp import plot, read


## =============================================================================
## Parameters
input_file = sys.argv[1]
plot_types = read.read_post_proc(input_file)[0]
n_atom_unit_cell = read.read_post_proc(input_file)[1]
Masses = read.read_post_proc(input_file)[2]
file_eigenvectors = read.read_post_proc(input_file)[3]
file_SPOSCAR = read.read_post_proc(input_file)[4]
max_Z = read.read_post_proc(input_file)[5]
freq_res = read.read_post_proc(input_file)[6]
kinput = read.read_post_proc(input_file)[7::][0]
labels = read.read_post_proc(input_file)[8]
modes = read.read_post_proc(input_file)[9]
temperatures_folders = read.read_post_proc(input_file)[10]



tot_atoms_uc = int(np.sum(n_atom_unit_cell)) 
Nqpoints, qpoints_scaled, ks, freqs_disp, eigvecs_phonopy, distances, Hk = read.read_phonopy(file_eigenvectors, tot_atoms_uc)
SCell, Ruc, R0, masses, masses_for_animation = read.read_SPOSCAR_and_masses(file_SPOSCAR, n_atom_unit_cell, n_atom_unit_cell, Masses)  
#### =============================================================================

for mode in plot_types:
    if(mode==0):
        namedir = plot.create_folder('')
        freq = np.loadtxt('ZS', usecols=0)
        meta = len(freq)
        for i in range(1):#(Nqpoints):
            to_skip = (1+meta)*i
            ZZ = np.genfromtxt('Zqs',skip_header=to_skip+1, max_rows=meta)
            Z_q = ZZ[:,0]
            Z = ZZ[:,1:]
            to_skip2 = 4*i
            Params = np.genfromtxt('quasiparticles',skip_header=to_skip2+1, max_rows=3)
            
    
            k_scaled = qpoints_scaled[i]
            eigvec = eigvecs_phonopy[i]
            freq_disp = freqs_disp[i]
            print(' Creating plots for k point = ', k_scaled)
            for n in range(tot_atoms_uc*3):
                params = Params[:,n]

                sig, mi = params[-1]/2, freq[int(len(freq)/2)]
                gaussian = 1/(sig*np.sqrt(2*np.pi)) * np.exp(-.5*((freq-mi)/sig)**2)
                convolution_lorentzian = signal.fftconvolve(Z[:,n], plot.lorentzian(freq, freq[int(len(freq)/2)], params[1], params[2]), mode='same') / sum( plot.lorentzian(freq, *params))
                convolution = signal.fftconvolve(Z[:,n],gaussian, mode='same') / sum( gaussian)
                plot.save_proj(freq,Z[:,n],Z_q, convolution, qpoints_scaled[i], Ruc, eigvec[:,n],freq_disp[n],n,namedir,masses_for_animation, params, max_Z)
    
    
    if(mode==1):
        freq = np.loadtxt('ZS', usecols=0)
        meta = len(freq)
        ZQS = [np.zeros(meta)]
        count = 1
        accepted_qpoints = []
        accepted_labels = []
        for i in range(Nqpoints):
            to_skip = (1+meta)*i
            qpoint = np.genfromtxt('Zqs',skip_header=to_skip+0, max_rows=1)
            for j in range(len(kinput)):
                if(np.allclose(qpoint, kinput[j]) and (qpoint.tolist() not in accepted_qpoints)):
                    accepted_qpoints.append(qpoint.tolist())
                    accepted_labels.append(labels[j])
                    Zq = np.genfromtxt('Zqs',skip_header=to_skip+1, max_rows=meta)
                    ZQS.append(Zq[:,0])
                    count = count + 1
                
                    #    Ztot = np.genfromtxt('ZS',usecols=0)
        ZQS = np.array(ZQS).T
        ZQS[:,0] = np.sum(ZQS[:,1::],axis=1)
        plot.plot1(freq,ZQS, accepted_labels)
        
        
    if(mode==2): 
        freq = np.loadtxt('ZS', usecols=0)
        meta = len(freq)
        ZQS = np.zeros((meta, tot_atoms_uc*3+1, len(kinput)))
        count = 0
        accepted_qpoints = []
        accepted_labels = []
        freqs_from_disp = np.zeros((tot_atoms_uc*3,len(kinput)))
        for i in range(Nqpoints):
            to_skip = (1+meta)*i
            qpoint = np.genfromtxt('Zqs',skip_header=to_skip+0, max_rows=1)
    
            for j in range(len(kinput)):
                if(np.allclose(qpoint, kinput[j]) and (qpoint.tolist() not in accepted_qpoints)):
                    accepted_qpoints.append(qpoint.tolist())
                    accepted_labels.append(labels[j])
    
                    for m in range(Nqpoints):
                        if(np.allclose(qpoint,qpoints_scaled[m])):
                            freqs_from_disp[:,count] = freqs_disp[m]
                            break
                    
                    
                    Zq = np.genfromtxt('Zqs',skip_header=to_skip+1, max_rows=meta)
                    ZQS[:,:,count] = Zq[:,:]
                    count = count + 1
                    
        
        plot.plot2(freq,ZQS, modes, accepted_labels, freqs_from_disp)
        
        
    if(mode==3):
        subdirectories = [x[1] for x in os.walk(temperatures_folders)][0]
        subdirectories.sort(key= lambda x: float(x.strip('K')))
        Ts = [int(x.strip('K')) for x in subdirectories]
        frequencies = np.zeros((2,tot_atoms_uc*3,len(kinput),len(Ts)))
        count_T = 0
        for subdir in subdirectories:
            count_q = 0
            accepted_qpoints = []
            accepted_labels = []
    
            for i in range(Nqpoints):
                to_skip = (4)*i
                qpoint = np.genfromtxt(temperatures_folders+subdir+'/quasiparticles',skip_header=to_skip+0, max_rows=1)
                for j in range(len(kinput)):
                    if(np.allclose(qpoint, kinput[j]) and (qpoint.tolist() not in accepted_qpoints)):
                        accepted_qpoints.append(qpoint.tolist())
                        accepted_labels.append(labels[j])
                        omegas_gammas = np.genfromtxt(temperatures_folders+subdir+'/quasiparticles',skip_header=to_skip+1, max_rows=3)
                        frequencies[:,:,count_q, count_T] = omegas_gammas[0::2,:]
                        count_q = count_q + 1
            count_T = count_T + 1
        
        diff =len(frequencies[0,0,:,0]) -  len(accepted_labels) 
        if(diff != 0): #this is to eliminate repetitive kpoints if present
            for h in range(diff):
                frequencies = np.delete(frequencies, -1, axis=2)
        plot.plot3(Ts, frequencies, modes, accepted_labels)
    
       
    if(mode==4):
        freq = np.loadtxt('ZS', usecols=0)
        meta = len(freq)
        # take the path the user inputs and find all the k points you can plot
        ks_path, x_labels, distances = read.read_path(kinput, Nqpoints, labels, Hk)
        frequencies = np.zeros((2,tot_atoms_uc*3,len(ks_path)))
        frequencies_disp = np.zeros((1,tot_atoms_uc*3,len(ks_path)))
        ZQS = np.zeros((meta, 1+len(ks_path))) #for the DOS
        
        count_DOS, count = 0, 0
        accepted_qpoints = []
        for i in range(Nqpoints):
            to_skip = (4)*i
            qpoint = np.genfromtxt('quasiparticles',skip_header=to_skip+0, max_rows=1)
            index_disp = np.min((np.argwhere(np.all(np.equal(qpoint, qpoints_scaled), axis=1))))
            if(np.any(np.all(np.equal(qpoint,ks_path), axis=1))): # e' un delirio questo ahaha, verifica che il qpoint trovato sia nel kpath
                params = np.genfromtxt('quasiparticles',skip_header=to_skip+1, max_rows=3)
                omegas_gammas = params[0::2,:]
                frequencies[:,:,count] = omegas_gammas
                frequencies_disp[:,:,count] = freqs_disp[index_disp,:]
                count = count + 1
            
            to_skip_DOS = (1+meta)*i
            for j in range(len(ks_path)):
                if(np.allclose(qpoint, ks_path[j]) and (qpoint.tolist() not in accepted_qpoints)):
                    accepted_qpoints.append(qpoint.tolist())
                    Zq = np.genfromtxt('Zqs',skip_header=to_skip_DOS+1, max_rows=meta)
                    ZQS[:,count_DOS+1] = Zq[:,0]
                    count_DOS = count_DOS + 1
                
        ZQS[:,0] = np.loadtxt('ZS', usecols=0)    
        plot.plot4(distances, frequencies, frequencies_disp, ks_path, x_labels, ZQS)
    
    if(mode==5):
        # take the path the user inputs and find all the k points you can plot
        ks_path, x_labels, distances = read.read_path(kinput, Nqpoints, labels, Hk) #you use this only to get x_labels, you should include this into read_phonopy
        num_modes = len(modes)
    
        
        freq = np.loadtxt('ZS', usecols=0)
        meta = len(freq)
        ZQS = np.zeros((meta, len(qpoints_scaled)))
        ZQS_proj = np.zeros((meta, num_modes, len(qpoints_scaled)))
        count = 0
        accepted_qpoints = []
        freqs_from_disp = np.zeros((len(qpoints_scaled),tot_atoms_uc*3))
        for i in range(Nqpoints):
            to_skip = (1+meta)*i
            qpoint = np.genfromtxt('Zqs',skip_header=to_skip+0, max_rows=1)
            for j in range(len(qpoints_scaled)):
                if(np.allclose(qpoint, qpoints_scaled[j]) and ((qpoint.tolist() not in accepted_qpoints) or i==j)): #è un completo delirio
                    accepted_qpoints.append(qpoint.tolist())
                    for m in range(Nqpoints):
                        if(np.allclose(qpoint,qpoints_scaled[m])):
                            freqs_from_disp[count, :] = freqs_disp[m,:]
                            break
                    Zq = np.genfromtxt('Zqs',skip_header=to_skip+1, max_rows=meta)
                    if(num_modes == tot_atoms_uc*3):
                        ZQS[:,count] = Zq[:,0]
                    else:
                        for b in range(len(modes)):
                            mm = modes[b]
                            ZQS_proj[:,b,i] = Zq[:,mm+1]
                    count = count + 1
        plot.plot_k2(freq,ZQS,ZQS_proj, x_labels,[freqs_from_disp],max_Z,modes, freq_res, title=['0K dispersion'])

    if(mode==6):
        # take the path the user inputs and find all the k points you can plot
        ks_path, x_labels, distances = read.read_path(kinput, Nqpoints, labels, Hk) #you use this only to get x_labels, you should include this into read_phonopy
        num_modes = len(modes)
        N_kpath = len(ks_path)
        
        freq = np.loadtxt('ZS', usecols=0)
        meta = len(freq)
        accepted_qpoints = []
        for i in range(Nqpoints):
            to_skip = (1+meta)*i
            qpoint = np.genfromtxt('Zqs',skip_header=to_skip+0, max_rows=1)
            for j in range(len(ks_path)):
                if(np.allclose(qpoint, ks_path[j]) and ((qpoint.tolist() not in accepted_qpoints) or i==j)): #è un completo delirio
                    accepted_qpoints.append(qpoint.tolist())
                    eigvec = eigvecs_phonopy[i]
                    freq_disp = freqs_disp[i]
                    Zq = np.genfromtxt('Zqs',skip_header=to_skip+1, max_rows=meta)
                    for b in range(len(modes)):
                        mm = modes[b]
                        ani = plot.plot6(freq,Zq[:,mm+1],Zq[:,0], np.dot(Hk,qpoint),eigvec[:,mm],freq_disp[mm],mm,Ruc,file_eigenvectors,masses_for_animation, max_Z)
        
        
        
    if(mode==7):
        print('WARNING: atm this only works for cubic crystals!')
        # take the path the user inputs and find all the k points you can plot
        ks_path, x_labels, distances = read.read_path(kinput, Nqpoints, labels, Hk) 
        
        c_A_to_B = 1.88973 #conversion to Bohrs
        Hk = Hk/(2*np.pi) #if you use Thz as frequencies, you have to use 1/B as k, without 2 pi
        Hk = Hk*c_A_to_B #if you wanna use the 1/100 conv factor later, you need Angstrom
        
        #find the closest qpoints for EC
        dirs_C11 = [[1,0,0],[0,1,0],[0,0,1]]
        dirs_C12_C44 = [[1,1,0],[1,0,1],[0,1,1]]
        ampl = 10
        
        A1, A2, A3 = SCell[0,:], SCell[1,:], SCell[2,:]
        V = np.dot(A1, np.cross(A2,A3))
        print('The volume of the supercell is ', V, 'Bohr^3')
        print('NB: if you run a NPE simulation, you better use the average NPE volume!')
        conv_to_gcm3 = 11.2059 #convert amu/B^3 to g/cm^3
        M_tot = np.sum(masses)/3
        rho = M_tot/V*conv_to_gcm3
        print('The density is ',rho, ' g/cm^3\n')
        
        conv_factor = 1/100        
        
        accepted_qpoints = []
        for i in range(1,len(ks_path)-1):
            eigvec_q = eigvecs_phonopy[i]
            
            qpoint_sc = ks_path[i]
            qpoint_sc_prev = ks_path[i-1]
            direc = np.abs(np.dot(Hk, qpoint_sc - qpoint_sc_prev))
            direc_sc = np.round(direc/direc.max(),2)

                
            to_skip = (4)*i
            qpoint = np.genfromtxt('quasiparticles',skip_header=to_skip+0, max_rows=1)
            if(direc_sc.tolist() in dirs_C11 and (np.allclose(qpoint_sc_prev,[0,0,0]) or np.allclose(ks_path[i+1],[0,0,0]))):
                
                params = np.genfromtxt('quasiparticles',skip_header=to_skip+1, max_rows=3)
                omegas  = params[0,:]
                
                csi = np.linalg.norm(np.dot(Hk,qpoint))
                print('csi: ', csi)
                print()
                ##==============================================================================
                ## C11
                print('# =============================================================================')
                print('C11')
                freqs = []
                eigvecs_acou = eigvec_q[:,0:3]
                for j in range(0,3):
                    freqs.append(omegas[j])
                    
                
                j = -1
                freq = freqs[j]
                eigvec = eigvecs_acou[:,j]
                print('qpoint scaled: ', qpoint)
                print('qpoint:', np.round(np.dot(Hk,qpoint),3))
                print()
                print('freqs: ', np.round(freqs,3), ' taken ', np.round(freq,3))
                print('\neigenvec:')
                print(np.round(eigvec*ampl/np.sqrt(masses_for_animation),2).reshape(np.shape(Ruc)))
                print('# =============================================================================')
                print()
                C11 = rho * (freq/csi)**2 *conv_factor
                ##==============================================================================
                
                # =============================================================================
                # C44
                print('# =============================================================================')
                print('C44-1')
                freqs = []
                eigvecs_acou = eigvec_q[:,0:3]
                for j in range(0,3):
                    freqs.append(omegas[j])
                j = 0
                freq = freqs[j]
                eigvec = eigvecs_acou[:,j]
                print('qpoint scaled: ', qpoint)
                print('qpoint: ',np.round(np.dot(Hk,qpoint),3))
                print()
                print(np.round(freqs,3), ' taken ', np.round(freq,3))
                print('\neigvec:')
                print(np.round(eigvec*ampl/np.sqrt(masses_for_animation),2))
                C44_1 = rho * (freq/csi)**2 *conv_factor
                print('# =============================================================================')
                print()
                # =============================================================================
                
                
            if(direc_sc.tolist() in dirs_C12_C44 and np.allclose(qpoint_sc_prev,[0,0,0]) or np.allclose(ks_path[i+1],[0,0,0])):
                params = np.genfromtxt('quasiparticles',skip_header=to_skip+1, max_rows=3)
                omegas  = params[0,:]
                
                #check that k = [csi, csi, 0]
                check = [np.allclose(x,csi) for x in np.dot(Hk,qpoint)] 
                if (check not in [[True, True, False],[True, False, True],[False, True, True]]):
                    print('ERROR WARNING: the q point is not [csi, csi, 0] so everything is gonna be wrong')
                
                
                
                # =============================================================================
                # C44
                print('# =============================================================================')
                print('C44-2')
                freqs = []
                eigvecs_acou = eigvec_q[:,0:3]
                for j in range(0,3):
                    freqs.append(omegas[j])
                j = 1
                freq = freqs[j]
                eigvec = eigvecs_acou[:,j]
                print('qpoint scaled: ', qpoint)
                print('qpoint:', np.dot(Hk,qpoint))
                print()
                print('freqs: ', freqs, ' taken ', freq)
                print('\neigenvec:')
                print(np.round(eigvec*ampl/np.sqrt(masses_for_animation),2).reshape(np.shape(Ruc)))
                print('# =============================================================================')
                print()
                C44_2 = .5* rho * (freq/csi)**2 *conv_factor
                # =============================================================
                
                
                #==============================================================================
                # C12
                print('# =============================================================================')
                print('C12-1')
                freqs = []
                eigvecs_acou = eigvec_q[:,0:3]
                for j in range(0,3):
                    freqs.append(omegas[j])
                    
                #csi = np.linalg.norm(np.dot(hr,qpoint_scaled))
                j = 0
                freq = freqs[j]
                eigvec = eigvecs_acou[:,j]
                print('qpoint scaled: ', qpoint)
                print('qpoint: ',np.round(np.dot(Hk,qpoint),3))
                print()
                print(np.round(freqs,3), ' taken ', np.round(freq,3))
                print('\neigvec:')
                print(np.round(eigvec*ampl/np.sqrt(masses_for_animation),2))
                A = rho * (freq/csi)**2 *conv_factor
                C12_1 =C11-A  #<- with freqs[0] # A - C11 -2*C44 #
                print('# =============================================================================')
                print()
                #==============================================================================
                
                #==============================================================================
                # C12
                print('# =============================================================================')
                print('C12-2')
                freqs = []
                eigvecs_acou = eigvec_q[:,0:3]
                for j in range(0,3):
                    freqs.append(omegas[j])
                    
                #csi = np.linalg.norm(np.dot(hr,qpoint_scaled))
                j = -1
                freq = freqs[j]
                eigvec = eigvecs_acou[:,j]
                print('qpoint: ', qpoint)
                print('qpoint:', np.dot(Hk,qpoint))
                print()
                print('freqs: ', freqs, ' taken ', freq)
                print('eigenvec:')
                print(np.round(eigvec*ampl/np.sqrt(masses_for_animation),2).reshape(np.shape(Ruc)))
                print('# =============================================================================')
                print()
                A = rho * (freq/csi)**2 *conv_factor
                C12_2 = A - C11 -2*C44_1 #C11-A  #<- with freqs[0] #
                C12_2_2 = A - C11 -2*C44_2
                #==============================================================================
                
                print()
                print('Elastic constants')
                print('C11 = ', np.round(C11,2), 'GPa')
                print('C44 using [100] = ', np.round(C44_1,2), 'GPa')
                print('C44 using [110] = ', np.round(C44_2,2), 'GPa')
                print('C12 using eq 1 = ', np.round(C12_1,2), 'GPa')
                print('C12 using eq 2 (C44[100])= ', np.round(C12_2,2), 'GPa')
                print('C12 using eq 2 (C44[110])= ', np.round(C12_2_2,2), 'GPa')
                
                print()
                print('Engineering elastic constants')
                ni = C12_2_2/(C11+C12_2_2)
                E = C11*(1+ni)*(1-2*ni)/(1-ni)
                print('E = ', np.round(E,2), 'GPa')
                print('ni = ', np.round(ni,2))
                print('G = ', np.round(C44_2,2), 'GPa')
        
        

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

