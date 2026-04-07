#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:53:57 2024

@author: aget
"""
import numpy as np
from yaml_class import yaml_proc
import argparse
import yaml
import json
import re
import subprocess as sp
from interpolation_a_PBE_cp2k import interpolation_a_PBE as cp2k_interpolation_a

def a_interpolation(x,y):
    xar=np.array([x,1-x])
    yar=np.array([1-y,y])
    Q=np.array([[11.51003,10.63214],[12.38362,11.73008]])
    return np.dot(yar,np.dot(Q,xar))

parser = argparse.ArgumentParser(description='params')
parser.add_argument('-x', dest='x', type=float, default=0.)
parser.add_argument('-y', dest='y', type=float, default=0.)
parser.add_argument('-N', dest='N', type=int,nargs=3, default=(3,3,3))
parser.add_argument('--yamlbase', dest='yaml_base', type=str, default='/home/fs71287/gentles/data/base.yaml')
parser.add_argument('--angstrom',dest='angstrom' ,action='store_true')
parser.add_argument('--base', dest='base', type=str, default='none')

args = parser.parse_args()

x=args.x
y=args.y

base_name=args.base

x=round(x,4)
y=round(y,4)
b1=len(str(x))-2
b2=len(str(x))-2

x1=round(1-x,4)
y1=round(1-y,4)

N=list(args.N)
yaml_base=args.yaml_base
print(x,x1,y1,y,N)
if base_name=='none':
    base="In%sGa%sAs%sSb%s_%sx%sx%s"%(x,x1,y1,y,N[0],N[1],N[2])
else:
    base=base_name

yaml_name="%s.yaml"%(base)

with open(yaml_base,'r') as fi:
    s=fi.read()
    
#a=a_interpolation(x,y)
if args.angstrom==True:
    a=cp2k_interpolation_a(x,y)
else:
    a=a_interpolation(x,y)

a_2=float(a/2)
p1=re.compile(r"species:\s+\[([A-Za-z, ]+)\]")
q1=p1.search(s)
#print(q1.group(1))
matches = re.findall(r'[^,]+', q1.group(1))
base_number=len(matches)

#print(len(matches))

#exit(1)
#base_number=8
Inn=int(round(int(base_number/2)*np.prod(N)*x))
Gan=int(round(int(base_number/2)*np.prod(N)-Inn))
Sbn=int(round(int(base_number/2)*np.prod(N)*y))
Asn=int(round(int(base_number/2)*np.prod(N)-Sbn))

s=re.sub('<N1>', str(N[0]), s)
s=re.sub('<N2>', str(N[1]), s)
s=re.sub('<N3>', str(N[2]), s)
s=re.sub('<a1>', str(a)   , s)
s=re.sub('<a2>', str(a_2), s)
s=re.sub('<Inn>', str(Inn), s)
s=re.sub('<Gan>', str(Gan), s)
s=re.sub('<Asn>', str(Asn), s)
s=re.sub('<Sbn>', str(Sbn), s)

with open(yaml_name,'w') as fo:
    fo.write(s)

runout=sp.run(['sqsgen run iteration %s'%yaml_name],shell=True)

ab=yaml_proc('%s.result.yaml'%(base),'%s.yaml'%base)
ab.prepare_lattice(a)
ab.to_crys('%s.crys'%base)
ab.to_xyz('%s.xyz'%base)
