#!/usr/bin/env python3

import numpy as np
import os
import re
import sys
import matplotlib.pyplot as plt
import h5py
from scipy.optimize import curve_fit

def bowing_curve(y, A, B, c):
    return A * y + B * (1 - y) + c * y * (1 - y)

def vegard_curve(x,A,B):
    return A*x+B*(1-x)

fixed_dict={'Ga_AsSb':['x',0.0],
            'In_AsSb':['x',1.0],
            'InGa_Sb':['y',1.0],
            'InGa_As':['y',0.0]}

donati_bowing={'Ga_AsSb':np.array([1.519,0.812,-1.43]),
               'In_AsSb':np.array([0.417,0.235,-0.67]),
               'InGa_Sb':np.array([0.812,0.235,-0.415]),
               'InGa_As':np.array([1.519,0.417,-0.477])}
for name in ['Ga_AsSb']:
    fig,ax=plt.subplots(1,1,figsize=(5,4))
    with h5py.File("GI_SR_3.results.hdf5", "r") as h5f:
        x_or_y=fixed_dict[name][0]
        other_x_or_y='y' if x_or_y=='x' else 'x'
        fixed_val=fixed_dict[name][1]
        ys=[]
        Eg_means=[]
        for i,group_name in enumerate(h5f.keys()):
            print(group_name)
            if f"{x_or_y}_{fixed_val}" in group_name:
                if i==0:
                    ax.scatter(h5f[group_name].attrs[other_x_or_y]*np.ones(h5f[f"{group_name}/Eg"][:].shape),h5f[f"{group_name}/Eg"][:],c='blue',label='all 3')
                else:
                    ax.scatter(h5f[group_name].attrs[other_x_or_y]*np.ones(h5f[f"{group_name}/Eg"][:].shape),h5f[f"{group_name}/Eg"][:],c='blue')
                mean_Eg = h5f[f"{group_name}/Eg"].attrs['mean']
                std_Eg = h5f[f"{group_name}/Eg"].attrs['std']
                var_Eg = h5f[f"{group_name}/Eg"].attrs['var']
                y_val = h5f[group_name].attrs[other_x_or_y]
                if i==0:
                    ax.errorbar(y_val, mean_Eg, yerr=std_Eg, fmt='o', color='r',label='means w/std')
                else:
                    ax.errorbar(y_val, mean_Eg, yerr=std_Eg, fmt='o', color='r')
                ys.append(y_val)
                Eg_means.append(mean_Eg)
        ys3=np.array(ys)
        Eg_means3=np.array(Eg_means)

    with h5py.File("GI_SR_2.results.hdf5", "r") as h5f:
        x_or_y=fixed_dict[name][0]
        other_x_or_y='y' if x_or_y=='x' else 'x'
        fixed_val=fixed_dict[name][1]
        ys=[]
        Eg_means=[]
        for i,group_name in enumerate(h5f.keys()):
            print(group_name)
            if f"{x_or_y}_{fixed_val}" in group_name:
                if i==0:
                    ax.scatter(h5f[group_name].attrs[other_x_or_y]*np.ones(h5f[f"{group_name}/Eg"][:].shape),h5f[f"{group_name}/Eg"][:],c='darkblue',label='exact 2')
                else:
                    ax.scatter(h5f[group_name].attrs[other_x_or_y]*np.ones(h5f[f"{group_name}/Eg"][:].shape),h5f[f"{group_name}/Eg"][:],c='darkblue')
                mean_Eg = h5f[f"{group_name}/Eg"].attrs['mean']
                std_Eg = h5f[f"{group_name}/Eg"].attrs['std']
                var_Eg = h5f[f"{group_name}/Eg"].attrs['var']
                y_val = h5f[group_name].attrs[other_x_or_y]
                if i==0:
                    ax.errorbar(y_val, mean_Eg, yerr=std_Eg, fmt='o', color='m',label='means w/std')
                else:
                    ax.errorbar(y_val, mean_Eg, yerr=std_Eg, fmt='o', color='m')
                ys.append(y_val)
                Eg_means.append(mean_Eg)
        ys2=np.array(ys)
        Eg_means2=np.array(Eg_means)

    with h5py.File("GI_SR_4D.results.hdf5", "r") as h5f:
        xs1=h5f['x'][:]
        ys1=h5f['y'][:]
        Eg1=h5f['Eg'][:]
    if x_or_y=='x':
        which_xs=np.where(xs1==fixed_val)[0]#
        print(which_xs)
        choice=ys1[which_xs]
    else:
        which_xs=np.where(ys1==fixed_val)[0]
        choice=xs1[which_xs]
    xs1=xs1[which_xs]
    ys1=ys1[which_xs]
    Eg1=Eg1[which_xs]
    print(x_or_y,choice,Eg1)
    
    #ax.scatter(choice,Eg1,c='g')

    params1,_=curve_fit(bowing_curve,ys2,Eg_means2)
    params2,_=curve_fit(bowing_curve,ys3,Eg_means3)
    #params2,_=curve_fit(bowing_curve,choice,Eg1)
    ax.plot(np.linspace(0., 1., 100),
                bowing_curve(np.linspace(0., 1., 100), donati_bowing[name][1], 
                            donati_bowing[name][0], donati_bowing[name][2]),
                label='Donati bowing %s' % donati_bowing[name][2], color='k')
    ax.plot(np.linspace(0., 1., 100),
                bowing_curve(np.linspace(0., 1., 100), params1[0], 
                            params1[1], params1[2]),
                label='DFT 2 %s' % params1[2], color='r',linestyle='--')
    ax.plot(np.linspace(0., 1., 100),
                bowing_curve(np.linspace(0., 1., 100), params2[0], 
                            params2[1], params2[2]),
                label='DFT 3 %s' % params2[2], color='purple',linestyle=':')
    #ax.plot(np.linspace(0., 1., 100),
    #            bowing_curve(np.linspace(0., 1., 100), params2[0], 
    #                        params2[1], params2[2]),
    #            label='old bowing %s' % params2[2], color='g',linestyle=':')
    ax.legend()
    ax.set_xlabel(x_or_y)
    ax.set_ylabel("Bandgap (eV)")
    ax.set_xlim(0., 1.)
    fig.savefig(f"{name}.bandgap.png", dpi=300)
