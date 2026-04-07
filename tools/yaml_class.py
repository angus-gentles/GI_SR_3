#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 12:48:41 2024

@author: aget
"""
import numpy as np
import yaml

class yaml_proc(object):
    def __init__(self,yaml_in,yaml_original):
        with open(yaml_in,'r') as fi:
            data=yaml.safe_load(fi)
            fi.close()
        self.data=data

        with open(yaml_original) as fj:
            data1=yaml.safe_load(fj)
            fj.close()
        self.sc=np.array(data1['structure']['supercell'])
        config_keys=[]
        arrangements=[]
        for key in self.data['configurations'].keys():
            config_keys.append(key)
            arrangements.append(self.data['configurations'][key])
        self.config_keys=config_keys
        self.arrangements=arrangements
        self.coords=np.array(data['structure']['coords'])
        self.lattice=np.array(data['structure']['lattice'])
        #print(self.data['structure'])
        self.species=self.data['structure']['species']
        self.which=np.array(data['which'])

    def prepare_lattice(self,a):
        self.lattice=self.lattice/self.lattice.max()
        self.lattice=self.lattice*self.sc
        self.lattice=self.lattice*a*0.5
            
    def to_xyz(self,xyz_out):
        types=np.array(self.species.copy())
        types[self.which]=np.array(self.arrangements[0]['configuration'])
        s="%s\ntest\n"%len(types)
        for i,coord in enumerate(self.coords):
            coor=self.lattice[0]*coord[0]+self.lattice[1]*coord[1]+self.lattice[2]*coord[2]
            s+="%s %s %s %s\n"%(types[i],coor[0],coor[1],coor[2])
        with open(xyz_out,'w') as fo:
            fo.write(s)
            fo.close()
        
    def to_xyz_all_configs(self,xyz_out):
        s=str()
        for j,types in enumerate(self.arrangements):
            s+="%s\ni=%s\n"%(len(types),j)
            for i,coord in enumerate(self.coords):
                coor=self.lattice[0]*coord[0]+self.lattice[1]*coord[1]+self.lattice[2]*coord[2]
                s+="%s %s %s %s\n"%(types[i],coor[0],coor[1],coor[2])
        with open('%s'%(xyz_out),'w') as fo:
            fo.write(s)
            fo.close()
            
    def to_xyz_all_seperate(self,xyz_out):
        for j,types in enumerate(self.arrangements):
            s=str()
            s+="%s\ni=%s\n"%(len(types),j)
            for i,coord in enumerate(self.coords):
                coor=self.lattice[0]*coord[0]+self.lattice[1]*coord[1]+self.lattice[2]*coord[2]
                s+="%s %s %s %s\n"%(types[i],coor[0],coor[1],coor[2])
            with open('%s_%s'%(j,xyz_out),'w') as fo:
                fo.write(s)
                fo.close()
        
    def to_crys_all_configs(self,crys_out):
        s=str()
        for j,types in enumerate(self.arrangements):
            s+="%s\ni=%s\n"%(len(types),j)
            for i,coord in enumerate(self.coords):
                #coor=lattice[0]*coord[0]+lattice[1]*coord[1]+lattice[2]*coord[2]
                s+="%s %s %s %s\n"%(types[i],coord[0],coord[1],coord[2])
        with open('%s'%(crys_out),'w') as fo:
            fo.write(s)
            fo.close()

    
    def to_crys_all_seperate(self,xyz_out):
        for j,types in enumerate(self.arrangements):
            s=str()
            s+="%s\ni=%s\n"%(len(types),j)
            for i,coord in enumerate(self.coords):
                #coor=lattice[0]*coord[0]+lattice[1]*coord[1]+lattice[2]*coord[2]
                s+="%s %s %s %s\n"%(types[i],coord[0],coord[1],coord[2])
            with open('%s_%s'%(j,xyz_out),'w') as fo:
                fo.write(s)
                fo.close()
    
    def to_crys(self,crys_out):
        #types=self.arrangements[0]['configuration']
        types=np.array(self.species.copy())
        types[self.which]=np.array(self.arrangements[0]['configuration'])
        s="%s\ntest\n"%len(types)
        for i,coord in enumerate(self.coords):
            s+="%s %s %s %s\n"%(types[i],coord[0],coord[1],coord[2])
        with open(crys_out,'w') as fo:
            fo.write(s)
            fo.close()
