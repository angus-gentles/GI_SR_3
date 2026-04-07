#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:23:27 2024

@author: gentles
"""

import yaml
import numpy as np


def yaml_to_xyz(yaml_in,xyz_out,lattice_out=False):
    with open(yaml_in,'r') as fi:
        data=yaml.safe_load(fi)
        fi.close()
    coords=np.array(data['structure']['coords'])
    lattice=np.array(data['structure']['lattice'])
    for key in data['configurations'].keys():
        key1=key
    types=data['configurations'][key1]
    s="%s\ntest\n"%len(types)
    for i,coord in enumerate(coords):
        coor=lattice[0]*coord[0]+lattice[1]*coord[1]+lattice[2]*coord[2]
        s+="%s %s %s %s\n"%(types[i],coor[0],coor[1],coor[2])
    with open(xyz_out,'w') as fo:
        fo.write(s)
        fo.close()
    if lattice_out==True:
        return lattice
    
def yaml_to_xyz_all_configs(yaml_in,xyz_out,lattice_out=False):
    with open(yaml_in,'r') as fi:
        data=yaml.safe_load(fi)
        fi.close()
    coords=np.array(data['structure']['coords'])
    lattice=np.array(data['structure']['lattice'])
    s=str()
    for j,key in enumerate(data['configurations'].keys()):
        key1=key
        types=data['configurations'][key1]
        s+="%s\ni=%s\n"%(len(types),j)
        for i,coord in enumerate(coords):
            coor=lattice[0]*coord[0]+lattice[1]*coord[1]+lattice[2]*coord[2]
            s+="%s %s %s %s\n"%(types[i],coor[0],coor[1],coor[2])
    with open('%s'%(xyz_out),'w') as fo:
        fo.write(s)
        fo.close()
    if lattice_out==True:
        return lattice
    
def yaml_to_crys_all_configs(yaml_in,xyz_out,lattice_out=False):
    with open(yaml_in,'r') as fi:
        data=yaml.safe_load(fi)
        fi.close()
    coords=np.array(data['structure']['coords'])
    lattice=np.array(data['structure']['lattice'])
    s=str()
    for j,key in enumerate(data['configurations'].keys()):
        key1=key
        types=data['configurations'][key1]
        s+="%s\ni=%s\n"%(len(types),j)
        for i,coord in enumerate(coords):
            #coor=lattice[0]*coord[0]+lattice[1]*coord[1]+lattice[2]*coord[2]
            s+="%s %s %s %s\n"%(types[i],coord[0],coord[1],coord[2])
    with open('%s'%(xyz_out),'w') as fo:
        fo.write(s)
        fo.close()
    if lattice_out==True:
        return lattice

#yaml_in='In0.5Ga0.5As1.0Sb0.0.result.yaml'
#xyz_out='test.xyz'
def yaml_to_crys(yaml_in,crys_out,lattice_out=False):
    with open(yaml_in,'r') as fi:
        data=yaml.safe_load(fi)
        fi.close()
    coords=np.array(data['structure']['coords'])
    lattice=np.array(data['structure']['lattice'])
    for key in data['configurations'].keys():
        key1=key
    types=data['configurations'][key1]
    s="%s\ntest\n"%len(types)
    for i,coord in enumerate(coords):
        s+="%s %s %s %s\n"%(types[i],coord[0],coord[1],coord[2])
    with open(crys_out,'w') as fo:
        fo.write(s)
        fo.close()
    if lattice_out==True:
        return lattice