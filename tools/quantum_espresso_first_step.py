#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 13:31:25 2024

@author: aget
"""

import numpy as np
import pymatgen as pmg
import json

from pymatgen.io.pwscf import PWInput
from pymatgen.core.structure import *
from yaml_class import yaml_proc

import argparse
from IGAS_supercell import IGAS_supercell

parser = argparse.ArgumentParser(description='params')
parser.add_argument('-x', dest='x', type=float, default=0.5)
parser.add_argument('-y', dest='y', type=float, default=0.5)
parser.add_argument('-N', dest='N', type=int,nargs=3, default=(3,3,3))
parser.add_argument('--yamlbase', dest='yaml_base', type=str, default='base.yaml')
parser.add_argument('--yamlresult', dest='yaml_result', type=str, default='none')
parser.add_argument('--crysresult', dest='crys_result', type=str, default='none')
parser.add_argument('--base', dest='base', type=str, default='none')
parser.add_argument('--nbnd', dest='nbnd', type=int, default=28)
parser.add_argument('--ksection', dest='ksection', type=str,default='ksection_relax_scf.txt')
parser.add_argument('--input_data', dest='input_data_file', type=str,default='input_data.json')
parser.add_argument('--pseudopotentials', dest='pseudopotentials_file', type=str,default='pseudopotentials.json')
parser.add_argument('--lattice_constant_file', dest='lattice_constant_file', type=str,default='a_base.json')
parser.add_argument('--U_file', dest='U_file', type=str,default='none')
args = parser.parse_args()

x=args.x
y=args.y
N=args.N
ksection=args.ksection
base_nbnd=args.nbnd
base_name=args.base
input_data_file=args.input_data_file
pseudopotentials_file=args.pseudopotentials_file
lattice_constant_file=args.lattice_constant_file
U_file=args.U_file
x=round(x,2)
y=round(y,2)

b1=len(str(x))-2
b2=len(str(x))-2

x1=round(1-x,2)
y1=round(1-y,2)


yaml_out_file=args.yaml_result
crys_out_file=args.crys_result
with open(input_data_file,'r') as fo:
    input_data=json.load(fo)
    fo.close()
print('x %s y %s N %s'%(x,y,N))
if base_name=="none":
    base="In%sGa%sAs%sSb%s_%sx%sx%s"%(x,x1,y1,y,N[0],N[1],N[2])
else:
    base=base_name
print('%s.U_in.json'%base)
#U={'In-5p':-1,'Ga-4p':-2,'As-4p':3,'Sb-5p':5}
if U_file=='none':
    with open('%s.U_in.json'%base,'r') as fo:
        U=json.load(fo)
        fo.close()
else:
    with open(U_file,'r') as fo:
        U=json.load(fo)
        fo.close()
with open(pseudopotentials_file,'r') as fi:
    pseudopotentials=json.load(fi)

with open(lattice_constant_file,'r') as fo:
    a=json.load(fo)

alat=x*y*a['InSb']+(1-x)*y*a['GaSb']+x*(1-y)*a['InAs']+(1-x)*(1-y)*a['GaAs']
alat*=N[0]
input_data['system']['celldm(1)']=alat
input_data['control']['prefix']=base
input_data['control']['outdir']='./tmp_%s'%base
input_data['system']['nbnd']=int(np.prod(np.array(N))*base_nbnd)

#with open('input_data.json','w') as fo:
#    json.dump(input_data,fo)

if crys_out_file=='none' and yaml_out_file=='none':
    exit('no out file to write from')
elif crys_out_file!='none' and yaml_out_file=='none':
    b=IGAS_supercell(base,U_in=U,input_data=input_data,crys_file=crys_out_file,
                     pseudopotentials=pseudopotentials,kgrid=[],ksection_file='ksection_relax_scf.txt')
elif crys_out_file=='none' and yaml_out_file!='none':
    b=IGAS_supercell(base,U_in=U,input_data=input_data,yaml_out_file=yaml_out_file,
                 pseudopotentials=pseudopotentials,kgrid=[],ksection_file='ksection_relax_scf.txt')
    #(self,base,U_in={},yaml_out_file='None',crys_file='None',
    #             input_data={},pseudopotentials={},kgrid=[],ksection_file='ksection.txt')
else:
    b=IGAS_supercell(base,U_in=U,input_data=input_data,crys_file=crys_out_file,
                     pseudopotentials=pseudopotentials,kgrid=[],ksection_file=ksection)

b.write('relax')
#b.calc()

