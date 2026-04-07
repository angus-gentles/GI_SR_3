#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 17:07:27 2024

@author: gentles
"""
import numpy as np
import pymatgen as pmg
import json
import re

from pymatgen.io.pwscf import PWInput
from pymatgen.core.structure import *
from yaml_class import yaml_proc

import argparse
from IGAS_supercell import IGAS_supercell

parser = argparse.ArgumentParser(description='params')
parser.add_argument('-x', dest='x', type=float, default=0.5)
parser.add_argument('-y', dest='y', type=float, default=0.5)
parser.add_argument('-N', dest='N', type=int,nargs=3, default=(3,3,3))
#parser.add_argument('--yamlbase', dest='yaml_base', type=str, default='base.yaml')
#parser.add_argument('--yamlresult', dest='yaml_result', type=str, default='base.result.yaml')
parser.add_argument('--base', dest='base', type=str, default='none')
parser.add_argument('--crysout', dest='crys_out', type=str, default='none')
parser.add_argument('--nbnd', dest='nbnd', type=int, default=28)
parser.add_argument('--ksection', dest='ksection_file', type=str, default='ksection_scf.txt')
parser.add_argument('--input_data', dest='input_data_file', type=str,default='input_data.json')
parser.add_argument('--pseudopotentials', dest='pseudopotentials_file', type=str,default='pseudopotentials.json')
parser.add_argument('--U_file', dest='U_file', type=str,default='none')
args = parser.parse_args()

x=args.x
y=args.y
N=args.N
base_name=args.base
ksection_file=args.ksection_file
input_data_file=args.input_data_file
pseudopotentials_file=args.pseudopotentials_file

U_file=args.U_file
x=round(x,4)
y=round(y,4)

b1=len(str(x))-2
b2=len(str(x))-2

x1=round(1-x,4)
y1=round(1-y,4)
if base_name=='none':
    base="In%sGa%sAs%sSb%s_%sx%sx%s"%(x,1-x,1-y,y,N[0],N[1],N[2])
else:
    base=base_name
base_nbnd=args.nbnd
crys_file=args.crys_out
#base_nbnd=18
p1=re.compile(r'alat=([0-9|.]+)')

with open(crys_file,'r') as fi:
    file1=fi.readlines()
    alat='none'
    for line in file1:
        line=line.strip()
        q1=p1.search(line)
        if q1:
            alat=float(q1.group(1))
if alat=='none':
    exit('no alat')
with open(input_data_file,'r') as fo:
    input_data=json.load(fo)
    fo.close()
#base="In%sGa%sAs%sSb%s_%sx%sx%s"%(x,x1,y1,y,N[0],N[1],N[2])

if U_file=='none':
    with open('%s.U_in.json'%base,'r') as fo:
        U=json.load(fo)
        fo.close()
else:
    with open(U_file,'r') as fo:
        U=json.load(fo)
        fo.close()
'''with open(lattice_constant_file,'r') as fo:
    a=json.load(fo)
    fo.close()'''

with open(pseudopotentials_file,'r') as fi:
    pseudopotentials=json.load(fi)

if crys_file=='none':
    crys_file='%s.out.crys'%base


input_data['control']['calculation']='scf'
input_data['control']['outdir']="./tmp_%s"%base
input_data['control']['prefix']=base
input_data['system']['celldm(1)']=alat
input_data['system']['nbnd']=int(np.prod(N)*int(base_nbnd*20/14))

b=IGAS_supercell(base,U_in=U,input_data=input_data,crys_file=crys_file,
                 pseudopotentials=pseudopotentials,kgrid=[],ksection_file=ksection_file)
b.write('scf')
#b.calc()
#input_data['control']['calculation']='nscf'
#input_data['control']['restart_mode']='restart'
#input_data['system']['nbnd']=int(np.prod(N)*int(base_nbnd*20/14))

#with open('input_data.json','w') as fo:
#    json.dump(input_data,fo)

#c=IGAS_supercell(base,U_in=U,input_data=input_data,crys_file=crys_file,
#                 pseudopotentials=pseudopotentials,kgrid=[8,8,8])
#c.write('nscf')
#c.calc()
