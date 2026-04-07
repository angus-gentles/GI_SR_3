#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:04:17 2024

@author: aget
"""
import json
from yaml_class import yaml_proc
import numpy as np
import os
from pymatgen.io.pwscf import PWInput
from pymatgen.core.structure import *
from yaml_class import yaml_proc
import subprocess as sp
from pymatgen.core.periodic_table import DummySpecies, Element, Species, get_el_sp


class IGAS_supercell(object):
    def __init__(self,base,U_in={},yaml_out_file='None',crys_file='None',
                 input_data={},pseudopotentials={},kgrid=[],ksection_file='ksection.txt'):
        self.U=U_in
        self.base=base
        yaml_original="%s.yaml"%base
        if crys_file=='None' and yaml_out_file=='None':
            raise ValueError('need crystal or sqsout file')
        elif crys_file!='None':
            coords=np.loadtxt(crys_file,skiprows=2,dtype=str)
            self.crys=coords[:,1:].astype(float)
            self.elements=coords[:,0]
        elif yaml_out_file!='None':
            a=yaml_proc(yaml_out_file,yaml_original)
            self.crys=a.coords
            self.elements=a.arrangements[0]
        else:
            exit('don\'t specify both crys and yaml_out')
        if len(input_data)==0 and os.path.exists('./input_data.json'):
            exit("no input data for QE")
        elif len(input_data)==0:
            with open('./input_data.json','r') as fi:
                input_data=json.load(fi)
        else:
            pass
        input_keys=[]
        for key in input_data.keys():
            input_keys.append(key)
        input_keys=np.array(input_keys)
        self.control=input_data['control']
        self.system=input_data['system']

        self.electrons=input_data['electrons']
        self.system['nat']=len(self.crys)
        
        if np.any(input_keys=='ions'):
            self.ions=input_data['ions']
        else: self.ions={}
        if np.any(input_keys=='cell'):
            self.cell=input_data['cell']
        else: self.cell={}
        if len(pseudopotentials)==0:
            with open('./pseudopotentials.json','r') as fi:
                self.pseudopotentials=json.load(fi)
        else:
            self.pseudopotentials=pseudopotentials
        self.kgrid=kgrid
        self.U=U_in
        self.system['ntyp']=len(self.pseudopotentials)
        if len(self.U)==0 and not os.path.exists('./U_in.json'):
            print('No U values present.')
        elif len(self.U)==0 and os.path.exists('./U_in.json'):
            with open('./U_in.json','r') as fi:
                self.U=json.load(fi)
        else:
            pass
        self.ksection=''
        if len(kgrid)==0 and os.path.exists(ksection_file):
            with open(ksection_file,'r') as fi:
                self.ksection=fi.read()
                fi.close()
                self.kmode='tpiba'
        elif len(kgrid)!=0 and os.path.exists(ksection_file):
            with open(ksection_file,'r') as fi:
                self.ksection=fi.read()
                fi.close()
                self.kmode='tpiba'
        elif len(kgrid)==0 and not os.path.exists(ksection_file):
            raise ValueError('path to ksection not found')
        else:
            self.kmode='automatic'
        lattice=[[1,0,0],[0,1,0],[0,0,1]]
        #coord_list=[DummySpecies("%s+"%coord) for coord in self.elements]
        self.b=Structure(lattice,self.elements, self.crys)
        
        

    def write(self,name='generic'):
        infile='%s.%s.in'%(self.base,name)
        self.name=name
        lattice=[[1,0,0],[0,1,0],[0,0,1]]
        #element_list=[]
        #for el in self.elements:
        #    element_list.append('%s%s'%(el[0],el[1]))
        #element_list=np.array(element_list)
        #print(element_list)
        self.b=Structure(lattice,self.elements, self.crys)
        a=PWInput(self.b,
            system=self.system,
            control=self.control,
            pseudo=self.pseudopotentials,
            electrons=self.electrons,
            cell=self.cell,
            ions=self.ions,
            kpoints_mode=self.kmode,
            kpoints_grid=self.kgrid)

        a.write_file(infile)
        with open(infile,'r') as fi:s=fi.read()
        s=re.sub('CELL_PARAMETERS[\S+\s+]+','',s)
        with open(infile,'w') as fi:fi.write(s)
        
        if len(self.ksection)!=0:
            with open(infile,'r') as fi:s=fi.read(); fi.close()
            s=re.sub('K_POINTS \S+',self.ksection,s)
            with open(infile,'w') as fi:fi.write(s) ; fi.close()
        U_section=str()
        with open(infile) as fi: s= fi.read()
        U_section+='HUBBARD (atomic)\n'
        for key in self.U.keys():
            if self.U[key]==0 : self.U[key]+=1e-06
            U_section+='U %s %s\n'%(key,self.U[key])
        s+=U_section
        s=re.sub('Ga\+','Ga1',s)
        s=re.sub('In\+','In1',s)
        s=re.sub('As\+','As1',s)
        s=re.sub('Sb\+','Sb1',s)
        s=re.sub('\+','',s)
        with open(infile,'w')as fo: fo.write(s)
        

    def calc(self):
        infile='%s.%s.in'%(self.base,self.name)
        outfile='%s.%s.out'%(self.base,self.name)
        this=sp.run('mpirun -np $SLURM_NPROCS pw.x < %s > %s'%(infile,outfile),shell=True)
        
        

            
        
